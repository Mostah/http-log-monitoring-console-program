"""
back.tests.test_statistics_manager

This module if for testing the statistics manager logic.
I use fake inputs and analyse either the outputs or the attributes.
"""

import pytest
from datetime import datetime

from ..log_pipeline.log_reader import LogReader
from .testdata import test_statistics_manager_data

class TestStatisticsManager:
    """
    This module if for testing the statistics manager logic.
    I use fake inputs and analyse either the outputs or the attributes.
    """
    
    # LogReader module is necessary for the alerter to work as it need its fictional time
    log_reader = LogReader()
    log_reader.fictional_time = datetime(2010,8,13,22,10,12)
    statistics_manager = log_reader.statistics_manager
    
    # fake data stored in testdata.py
    logs = test_statistics_manager_data['logs']
    general_batch = test_statistics_manager_data['general_batch']
    sections_batch = test_statistics_manager_data['section_batch']
    general_hits = test_statistics_manager_data['general_hits']
    section_hits = test_statistics_manager_data['section_hits']
    
    def test_remove_outdated_data_general_batch(self):
        """ Check if the outdated data are removed from general batch """
        
        self.statistics_manager.general_batch = self.general_batch
        self.statistics_manager._remove_outdated_data()
        assert len(self.statistics_manager.general_batch) == 4
        
    def test_remove_outdated_data_sections_batch(self):
        """ Check if the outdated data are removed from sections batch """
        
        self.statistics_manager.sections_batch = self.sections_batch
        self.statistics_manager._remove_outdated_data()
        assert len(self.statistics_manager.sections_batch['api']) == 2
        assert len(self.statistics_manager.sections_batch['report']) == 0
        
    def test_remove_outdated_data_general_hits(self):
        """ Check if the outdated data are removed from general hits """
        
        self.statistics_manager.general_hits = self.general_hits
        self.statistics_manager._remove_outdated_data()
        assert len(self.statistics_manager.general_hits) == 2
        
    def test_remove_outdated_data_sections_hits(self):
        """ Check if the outdated data are removed from sections hits """
        
        self.statistics_manager.sections_hits = self.section_hits
        self.statistics_manager._remove_outdated_data()
        assert len(self.statistics_manager.sections_hits['api']) == 3
        assert len(self.statistics_manager.sections_hits['report']) == 1
        
    def test_get_section(self):
        """ Check that it find the right section of a request """
        
        assert self.statistics_manager._get_section(self.logs[0]) == 'api'
        assert self.statistics_manager._get_section(self.logs[1]) == 'api'
        assert self.statistics_manager._get_section(self.logs[2]) == 'report'
        
    def test_get_batch_hits_section(self):
        """ Check that it computes the right hits for each sections """
        
        assert self.statistics_manager._get_batch_hits(self.sections_batch['api'], 'api') == 0.2
        assert self.statistics_manager._get_batch_hits(self.sections_batch['report'], 'report') == 0
        
    def test_get_batch_hits_general(self):
        """ Check that it computes the right hits for general """
        
        assert self.statistics_manager._get_batch_hits(self.general_batch) == 0.3