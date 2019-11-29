"""
back.log_pipeline.log_reader

Module, first bloc of the pipeline, that read logs from a file and convoy them through the pipeline.
"""
import re
import csv
from threading import Lock, Thread
from datetime import datetime, timedelta
import time


class LogReader(Thread):
    """ Module, first bloc of the pipeline, that read logs from a file and convoy them through the pipeline.
    
    Attributes
    ----------
    file : str, optional
        the file location of the logs, a sample by default 
    running : bool
        the process status of the reader
    time_difference : timedelta
        time difference between between the current time and when the logs where written
    fictional_time : datetime
        scenario time, calculated with the time_difference and the current time
    FIELDS_NAMES : list
        list of fields name from logs
        
    Methods
    -------
    start_reading() : 
        method that start the process of reading logs from the file
    stop_reading() : 
        method that stop the process of reading logs from the file
    """

    FIELDS_NAMES = ["remotehost","rfc931","authuser","date","request","status","bytes"]  
    
    def __init__(self, file = '../logs/sample_csv.txt'):
        """
        Parameters
        ----------
        file : str, optional
            the file location of the logs, a sample by default 
        """
        
        # instanciation of the parent
        Thread.__init__(self)
        self.daemon = True
        
        # status of the reader
        self.file = file
        self.running = True
        
        # for the purpose of running a scenario from a log file
        self.time_difference = None #timedelta
        self.fictional_time = None #datetime
        
        # next element of the pipeline
        self.statistics_manager = StatisticsManager()
    
    def start_reading(self):
        """method that start the process of reading logs from the file
        """
        
        # security to avoid race if at some point of the development log are generated and written in the log file
        with Lock():
            # this way it doesn't load the file in memory but create an iterable object from which we can load selected line in memory
            with open(self.file, 'r') as logs: 
                while self.running:
                    try:
                        # iterates over the lines, the previous one is garbage collected
                        line = logs.__next__() 
                        
                        #create a dict representing the currentlog
                        log = { self.FIELDS_NAMES[i]: value for i, value in enumerate(csv.reader([line]).__next__()) }
                        
                        if self._is_formatted(log):
                            #if time_difference is not define yet
                            if not self.time_difference: 
                                self.time_difference = datetime.now() - datetime.fromtimestamp(int(log['date'])) 
                                self.fictional_time = datetime.now() - self.time_difference
                                
                            # logs are not in order but I assume there is no more 3s difference between two successive log
                            # thus it has no major impact in the stats computation as it is over 10s
                            while self.fictional_time < datetime.fromtimestamp(int(log['date'])): 
                                time.sleep(0.2)
                                self.fictional_time = datetime.now() - self.time_difference
                                
                            # transfer the log through the next in the pipeline 
                            self.statistics_manager.push_log(log)
                    
                    except StopIteration:
                        # waiting for more lines
                        time.sleep(0.1)
    
    def stop_reading(self):
        """method that stop the process of reading logs from the file
        """
        self.running = False
         
    #TODO discard improperly formatted lines, unformated lines: if rest key of none value in field names, and check each value of each field with regex
    def _is_formatted(self, log):
        return True
    
LogReader().start_reading()