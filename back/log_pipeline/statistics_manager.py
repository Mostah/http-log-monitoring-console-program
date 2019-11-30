"""
back.log_pipeline.statistics_manager

Module, second bloc of the pipeline, that compute the stats for all sections
and the general information and then send them through a service
"""

class StatisticsManager:
    
    def __init__(self):
        self.batch = []
    
    def push_logs(self, batch):
        for e in batch:
            print(e)
        #self.batch = batch + self.batch
        
    def _general_statistics(self):
        pass
    
    def _sections_statistics(self):
        pass
    
    def _get_section(self, log):
        pass    
    
    def _get_section_hits(self,section):
        pass
    
    def _get_section_average10(self, section):
        pass
        
    def _get_section_average60(self, section):
        pass
        
    def _get_section_unique_hosts(self, section):
        pass
        
    def _get_section_total_bytes(self, section):
        pass
        
    def _get_section_availability(self, section):
        pass
    
    def _get_section_codes_count(self, section):
        pass
    
    def _get_general_hits(self):
        pass

    def _get_general_minimum_hits(self):
        pass
    
    def _get_general_average_hits(self):
        pass
    
    def _get_general_maximum_hits(self):
        pass
        
    def _get_general_availability(self):
        pass
    
    def _get_general_unique_hosts(self):
        pass
    
    def _get_general_total_bytes(self):
        pass