"""
back.tests.test_statistics_manager

This module if for testing the statistics computation of all our datastructures.
I use fake inputs and analyse either the outputs.
"""

import pytest

from ..log_pipeline.statistics import Statistics
from .testdata import test_statistics_data

class TestStatistics:
    """ This module if for testing the statistics computation of all our 
    datastructures. I use fake inputs and analyse either the outputs.
    """
    
    batch = test_statistics_data["batch"]
    time_length = 10
    hits = test_statistics_data["hits"]
    metrics_batch = test_statistics_data["metrics_batch"]

    def test_get_batch_hits_empty_batch(self):
        assert Statistics.get_batch_hits([],self.time_length) == 0
        
    def test_get_batch_hits_time_zero(self):
        assert Statistics.get_batch_hits(self.batch,0) == 0
        
    def test_get_batch_hits(self):
        assert Statistics.get_batch_hits(self.batch,2) == 2.5
        
    def test_get_unique_hosts_empty_batch(self):
        assert Statistics.get_unique_hosts([]) == 0
        
    def test_get_unique_hosts(self):
        assert Statistics.get_unique_hosts(self.batch) == 4
         
    def test_get_total_bytes_empty_batch(self):
        assert Statistics.get_total_bytes([]) == 0
        
    def test_get_total_bytes(self):
        assert Statistics.get_total_bytes(self.batch) == 5
              
    def test_get_availability_empty_batch(self):
        assert Statistics.get_availability([]) == 1
             
    def test_get_availability(self):
        assert Statistics.get_availability(self.batch) == 0.6
        
    def test_get_hits_average_empty_hits(self):
        assert Statistics.get_hits_average([]) == 0
        
    def test_get_hits_average(self):
        assert Statistics.get_hits_average(self.hits) == 5.25
        
    def test_get_minimum_hits_empty_hits(self):
        assert Statistics.get_minimum_hits([]) == 0
        
    def test_get_minimum_hits(self):
        assert Statistics.get_minimum_hits(self.hits) == 1
        
    def test_get_maximum_hits_empty_hits(self):
        assert Statistics.get_maximum_hits([]) == 0
        
    def test_get_maximum_hits(self):
        assert Statistics.get_maximum_hits(self.hits) == 12
        
    def test_get_average_metrics_hits_empty_batch(self):
        assert Statistics.get_average_metrics_hits([]) == 0
        
    def test_get_average_metrics_hits(self):
        assert Statistics.get_average_metrics_hits(self.metrics_batch) == 11.2
    

