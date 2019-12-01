"""
back.log_pipeline.metrics

Module that contain the GeneralMetrics for the general traffic information 
and the SectionMetrics for the section traffic information
"""

class GeneralMetrics:
    """ 
    Class that represent general stats from a batch of log
    
    Attributes
    ----------
    time : datetime
        time from the log for this batch of stats
    hits : int
        hits per seconds calculated over last 10 sec
    minimum : int
        minimum hits per seconds encountered over the selected timeframe
    average : int
        average of hits per second over the selected timeframe
    maximum : int
        maximum hits per seconds encountered over the selected timeframe
    availability : float
        availability over the selected timeframe
    unique_hosts : int
        number of different hosts calculated over selected timeframe
    total_bytes : int
        number of bytes transfered over selected timeframe
    """
    
    def __init__(self,time, hits, minimum, average, maximum, availability, unique_hosts, total_bytes):
        """
        Parameters
        ----------
        time : datetime
            time from the log for this batch of stats
        hits : int
            hits per seconds calculated over last 10 sec
        minimum : int
            minimum hits per seconds encountered over the selected timeframe
        average : int
            average of hits per second over the selected timeframe
        maximum : int
            maximum hits per seconds encountered over the selected timeframe
        availability : float
            availability over the selected timeframe
        unique_hosts : int
            number of different hosts calculated over the selected timeframe
        total_bytes : int
            number of bytes transfered over the selected timeframe
        """
            
        self.time = time
        self.hits = hits
        self.minimum = minimum
        self.average = average
        self.maximum = maximum
        self.availability = availability
        self.unique_hosts = unique_hosts
        self.total_bytes = total_bytes
        
    def __repr__(self):
        return "TIME: %s   HITS: %s/s   MINIMUM: %s/s   AVERAGE: %s/s   MAXIMUM: %s/s   AVAILABILITY: %s   UNIQUE_HOSTS: %s   TOTAL_BYTES: %sKB" \
            % (self.time,
                  self.hits,
                  self.minimum,
                  self.average,
                  self.maximum,
                  self.availability,
                  self.unique_hosts,
                  self.total_bytes
                )
            
class SectionMetrics:
    """ 
    Class that represent a section stats from a batch of log
    
    Attributes
    ----------
    section : str
        section this entry is about
    time : datetime
        time from the log for this batch of stats
    hits : int
        hits per seconds calculated over last 10 sec
    average : int
        average of hits per second over the given timeframe
    unique_hosts : int
        number of different hosts calculated over selected timeframe
    total_bytes : int
        number of bytes transfered over the selected timeframe
    availability : float
        availability over the selected timeframe
    error_codes_count : str
        error status codes over the selected timeframe
    """
    
    def __init__(self, section, time, hits, average, unique_hosts, total_bytes, availability, error_codes_count):
        """
        Parameters
        ----------
        section : str
            section this entry is about
        time : datetime
            time from the log for this batch of stats
        hits : int
            hits per seconds calculated over last 10 sec
        average : int
            average of hits per second over the given timeframe
        unique_hosts : int
            number of different hosts calculated over selected timeframe
        total_bytes : int
            number of bytes transfered over selected timeframe
        availability : float
            availability over the selected timeframe
        error_codes_count : str
            error status codes over the selected timeframe
        """
        
        self.section = section
        self.time = time
        self.hits = hits
        self.average = average
        self.unique_hosts = unique_hosts
        self.total_bytes = total_bytes
        self.availability = availability
        self.error_codes_count = error_codes_count

    def __repr__(self):
        return "SECTION: %s   TIME: %s   HITS: %s/s   AVERAGE: %s/s   UNIQUE_HOSTS: %s   TOTAL_BYTES: %sKB   AVAILABILITY: %s   ERROR_CODES_COUNT: %s" \
            % (self.section,
                self.time,
                self.hits,
                self.average,
                self.unique_hosts,
                self.total_bytes,
                self.availability,
                self.error_codes_count
              )