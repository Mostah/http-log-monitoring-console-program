"""
back.log_pipeline.statistics_manager

Module, second bloc of the pipeline, that compute the stats for all sections
and the general information, and then send them to the alerter and the service.
"""

from datetime import datetime, timedelta

from .metrics import GeneralMetrics, SectionMetrics
from .statistics import Statistics
from .service import Service
from .alerter import Alerter

class StatisticsManager:
    """
    Module, second bloc of the pipeline, that compute the stats for all sections
    and the general information, and then send them to the alerter and the service.
    
    Attributes
    ----------
    log_reader : LogReader
        a reference to the log reader to get access to the fictional time
    timeframe : int
        timeframe in minutes over with the stats are computer
    general_batch : list
        batch of log for stats of general information
    section_batch : dict
        batch of log for stats of all the sections
    general_metrics : GeneralMetrics
        general metric computed from general batch
    section_metrics : dict
        general section metrics computed from section batch
    general_hits : list
        list that keeps track of hits from general information to compute average, min and max
    section_hits : dict
        dict of lists that keep track of hits from section information to compute average
    service : Service
        one of the next module of the pipeline, it convey the metrics to the database
    alerter : Alerter
        one of the next module of the pipelie, it trigger alert if necessary

    
    Methods
    -------
    push_logs()
        push formatted batch of log into the current batch, get rid of the old logs, compute statistics
        and send them through the next elements of the pipeline 
    
    """
    
    def __init__(self, log_reader, timeframe):
        """
        Parameters
        ----------
        log_reader : LogReader
            a reference to the log reader to get access to the fictional time
        timeframe : int
            timeframe in minutes over with the stats are computer
        """
        
        self.log_reader = log_reader
        self.TIMEFRAME = timeframe
        
        # batch use to compute metrics
        self.general_batch = []
        self.sections_batch = { }
        self.general_hits = []
        self.sections_hits = { }
        
        # contain the actual metrics
        self.general_metrics = None
        self.sections_metrics = { }

        # next blocs of the pipeline
        self.service = Service()
        self.alerter = Alerter(log_reader)

        
    
    def push_logs(self, batch):
        """
        push formatted batch of log into the current batch, get rid of the old logs, compute statistics
        and send them through the next elements of the pipeline 
        """
        
        # add the new logs to the general batch
        self.general_batch = batch + self.general_batch
        
        # add every log to its section batch
        for log in batch:
            section = self._get_section(log)
            try:
                self.sections_batch[section].insert(0,log)
            except KeyError:
                self.sections_batch[section] = [log]

        # clean all batchs from outdated metrics
        self._remove_outdated_data()
        
        # compute the different metrics
        self._compute_sections_metrics()
        self._compute_general_metrics()

        # send new metrics to the next blocs of the pipeline
        self.service.add_general_metrics(self.general_metrics)
        self.service.add_sections_metrics(self.sections_metrics)
        self.alerter.push_metrics(self.sections_metrics)
    
    def _remove_outdated_data(self):
        """
        Remove the outdated metrics from all the data use to compute statistics over the selected timeframe
        """
        now = self.log_reader.fictional_time
        
        # remove outdated logs (that happened outside of the given timeframe) from the general batch
        self.general_batch = [log for log in self.general_batch 
                                    if (now - datetime.fromtimestamp(int(log['date']))) < timedelta(minutes = self.TIMEFRAME)]
        
        # remove outdated logs (that happened outside of the given timeframe) from all the section batchs
        for section, batch in self.sections_batch.items():
            self.sections_batch[section] = [log for log in batch 
                                                if (now - datetime.fromtimestamp(int(log['date']))) < timedelta(minutes = self.TIMEFRAME)]
        
        # remove outdated hits (that happened outside of the given timeframe) from the general hits
        self.general_hits = [hits for hits in self.general_hits 
                                    if now - hits['time'] < timedelta(minutes = self.TIMEFRAME)]
        
        # remove outdated hits (that happened outside of the given timeframe) from all the section hits
        for section, batch in self.sections_hits.items():
            self.sections_hits[section] = [hits for hits in batch
                                                if now - hits['time'] < timedelta(minutes = self.TIMEFRAME)]
                
                
    # TODO min is not right at the begining (<10s) as there is not enough data to compute the right hits
    def _compute_general_metrics(self):
        """compute the metrics for the general information"""
        
        self.general_metrics = GeneralMetrics (
            time = self.log_reader.fictional_time,
            hits = self._get_batch_hits(self.general_batch),
            minimum = Statistics.get_minimum_hits(self.general_hits),
            average = Statistics.get_hits_average(self.general_hits),
            maximum = Statistics.get_maximum_hits(self.general_hits),
            availability = Statistics.get_availability(self.general_batch),
            unique_hosts = Statistics.get_unique_hosts(self.general_batch),
            total_bytes = Statistics.get_total_bytes(self.general_batch),
        )
    
    def _compute_sections_metrics(self):
        """compute the metrics for the general information"""
        
        self.sections_metrics = {section: SectionMetrics(
            section = section,
            time = self.log_reader.fictional_time,
            hits = self._get_batch_hits(batch, section),
            average = Statistics.get_hits_average(self.sections_hits[section]),
            unique_hosts = Statistics.get_unique_hosts(batch),
            total_bytes = Statistics.get_total_bytes(batch),
            availability = Statistics.get_availability(batch),
            error_codes_count = '  '.join([key + ': ' + str(value) for key, value in Statistics.get_codes_count(batch).items() if int(key) > 300])
        ) for section, batch in self.sections_batch.items()}

    
    # TODO Implement regex instead of this ugly code
    @staticmethod
    def _get_section(log):
        """parse the section of a log
        
        Attributes
        ----------
        log : dict
            formatted log into a dict
        """
        
        section = ''
        section_found = False
        for char in log['request']:
            if char == '/' and not section_found:
                section_found = True
            elif char in ['/', ' ']  and section_found:
                break
            elif section_found:
                section += char
        return section
    
    
    def _get_batch_hits(self, batch, section = ''):
        """ compute average hits over the last 10s and store them in the proper attribute
        
        Attributes
        ----------
        batch : list
            list of log 
        section : str, optional
            section of this batch, if not given then considered as the general batch
        """
        
        now = self.log_reader.fictional_time
        
        # logs for the last 10 seconds
        batch10 = [log for log in batch
                            if (now - datetime.fromtimestamp(int(log['date']))) < timedelta(seconds = 10)]
        
        # number of hits/s for the last 10 seconds
        hits = Statistics.get_batch_hits(batch10, 10)
        
        # append calculated hits to the appropriate data structures
        if section == '':
            self.general_hits.append({'number': hits, 'time': now})
        else:
            try:
                self.sections_hits[section].append({'number': hits, 'time': now})
            except KeyError:
                self.sections_hits[section] = [{'number': hits, 'time': now}]
        
        return hits
    
    