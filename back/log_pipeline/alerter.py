"""
back.log_pipeline.alerter

Module, third bloc of the pipeline, that trigger an alert when necessary
"""

from datetime import timedelta
from .statistics import Statistics
from .service import Service

class Alerter():
    """ 
    Module that trigger an alert when necessary
    
    Attributes
    ----------
    log_reader : LogReader
        a reference to the log reader to get access to the fictional time
    TIME_WINDOW : int
        timeframe use to compute the stats
    THRESHOLD : int
        number of hits per second use as a reference to raise or drop an alert
    section_metrics_batch : dict
        dict of metrics within the time window use to change the alerting state of all sections
    sections_on_alert : dict
        dict of boolean representing the alerting state of all sections
    service : Service
        the next module of the pipeline, it sends the alert to the database
        
    Methods
    -------
    push_metrics()
        push formatted batch of metrics into the current batch, get rid of the old metrics, and raise
        or drop an alert if necessary
    """
    
    def __init__(self, log_reader, time_window = 2, threshold = 10):
        """
        Parameters
        ----------
        log_reader : LogReader
            a reference to the log reader to get access to the fictional time
        TIME_WINDOW : int, optional
            timeframe use to compute the stats
        THRESHOLD : int, optional
            number of hits per second use as a reference to raise or drop an alert
        """
        
        self.log_reader = log_reader
        self.TIME_WINDOW = time_window
        self.THRESHOLD = threshold
        
        # batch of metrics over the time_window for all sections
        self.section_metrics_batch = { }
        
        # boolean about the alerting state of all section
        self.sections_on_alert = { }
        
        # send alert to the next blocs of the pipeline
        self.service = Service()

        
    def push_metrics(self, sections_metrics):
        """
        push formatted batch of metrics into the current batch, get rid of the old metrics, and raise
        or drop an alert if necessary
        
        Parameters
        ----------
        section_metrics_batch : dict
            dict of metrics to be added to the current batch
        """
        
        # add metrics to existing section or a new one create one
        for section, metrics in sections_metrics.items():
            try:
                self.section_metrics_batch[section].insert(0,metrics)
            except KeyError:
                self.section_metrics_batch[section] = [metrics]
                self.sections_on_alert[section] = False
        
        # remove metrics that are not within the timeframe anymore
        self._remove_outdated_metrics()
        
        # raise or drop an alert if necessary for each section
        for section in self.sections_on_alert.keys():
            if not(self.sections_on_alert[section]) and self._is_high(section):
                self._raise_alert(section)
            elif self.sections_on_alert[section] and self._is_normal(section):
                self._drop_alert(section)
        
    def _remove_outdated_metrics(self):
        """
        Remove the outdated metrics from all the sections if they are not in the time window
        """
        
        now = self.log_reader.fictional_time
        for section, batch in self.section_metrics_batch.items():
            self.section_metrics_batch[section] = [metrics for metrics in batch 
                                                if (now - metrics.time) < timedelta(minutes = self.TIME_WINDOW)]
        
    def _is_high(self, section):
        """
        return if the traffic is 5% above the giving threshold
        """
        
        return Statistics.get_average_metrics_hits(self.section_metrics_batch[section]) > 1.05 * self.THRESHOLD
    
    def _is_normal(self, section):
        """
        return if the traffic is 5% below the giving threshold
        """
        
        return Statistics.get_average_metrics_hits(self.section_metrics_batch[section]) < 0.95 * self.THRESHOLD
    
    def _raise_alert(self, section):
        """
        change the alerting state of the section and send an alert through the service
        """
        
        self.sections_on_alert[section] = True
        alert = {
            'section': section,
            'status': 1,
            'hits': Statistics.get_average_metrics_hits(self.section_metrics_batch[section]),
            'time': self.log_reader.fictional_time
        }
        self.service.send_alert(alert)
    
    def _drop_alert(self, section):
        """
        change the alerting state of the section and send an alert through the service
        """
        
        self.sections_on_alert[section] = False
        alert = {
            'section': section,
            'status': 0,
            'hits': Statistics.get_average_metrics_hits(self.section_metrics_batch[section]),
            'time': self.log_reader.fictional_time
        }
        self.service.send_alert(alert)