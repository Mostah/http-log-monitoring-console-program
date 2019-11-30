"""
back.log_pipeline.statistics

Module that contain every statistical function use by the statistic manager module.
"""

from collections import Counter

class Statistics:
    """ Usefull methods that return statistics over batch and hits
    
    Methods
    -------
    get_batch_hits()
        return the number of hits per second
    get_unique_hosts()
        return the number of unique hosts
    get_total_bytes()
        return the sum of all bytes transfered by the logs in the batch in KB
    get_availability()
        return the availability, availability : a url is available if its status is < 300
    get_codes_count()
        return a dict containing the count of every HTTP code encountered
    get_hits_average
        return the average hits of the given list
    get_minimum_hits
        return the minimum hits of the given list
    get_maximum_hits
        return the maximum hits of the given list
     """
    
    @staticmethod
    def get_batch_hits(batch, time_length):
        """return the number of hits per second
        
        Parameters
        ----------
        batch
            list of formatted logs
        time_length
            period over which the stat is computed
        """
        
        if len(batch) == 0:
            return 0
        return len(batch) / time_length
    
    @staticmethod
    def get_unique_hosts(batch):
        """return the number of unique hosts
        
        Parameters
        ----------
        batch
            list of formatted logs
        """
        
        if len(batch) == 0:
            return 0
        unique_hosts = set([log['remotehost'] for log in batch])
        return len(unique_hosts)
    
    @staticmethod
    def get_total_bytes(batch):
        """ return the sum of all bytes transfered by the logs in the batch in KB 
        
        Parameters
        ----------
        batch : list
            list of formatted logs
        """
        
        if len(batch) == 0:
            return 0
        return int(sum([int(log['bytes']) for log in batch])/1000)
    
    @staticmethod
    def get_availability(batch):
        """ return the availability, availability : a url is available if its status is < 300
        
        Parameters
        ----------
        batch : list
            list of formatted logs
        """
        
        if len(batch) == 0:
            return 1
        return len([log for log in batch if int(log['status']) < 300])/len(batch)
    
    @staticmethod
    def get_codes_count(batch):
        """ return a dict containing the count of every HTTP code encountered
        
        Parameters
        ----------
        batch : list
            list of logs
        """
        
        batch_codes = [log['status'] for log in batch]
        return Counter(batch_codes)
    
    @staticmethod
    def get_hits_average(hits):
        """ return the minimum hits of the given list
        
        Parameters
        ----------
        hits : list
            list of formatted hits
        """
        
        if len(hits) == 0:
            return 0
        return sum([hit['number'] for hit in hits]) / len(hits)
    
    @staticmethod
    def get_minimum_hits(hits):
        """ return the minimum hits of the given list
        
        Parameters
        ----------
        hits : list
            list of formatted hits
        """
        
        if len(hits) == 0:
            return 0
        return min([hit['number'] for hit in hits])
    
    @staticmethod
    def get_maximum_hits(hits):
        """ return the maximum hits of the given list
        
        Parameters
        ----------
        hits : list
            list of formatted hits
        """
        
        if len(hits) == 0:
            return 0
        return max([hit['number'] for hit in hits])
