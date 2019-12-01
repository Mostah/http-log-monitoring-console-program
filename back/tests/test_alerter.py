"""
back.tests.test_alerter

This module if for testing the alerting logic by running tests over
the methods defined in alerter.py. I use fake inputs and analyse either the 
outputs or the attributes.
"""


import pytest
from datetime import datetime

from ..log_pipeline.log_reader import LogReader
from .testdata import test_alerter_data

class TestAlerter:
    """
    This module if for testing the alerting logic by running tests over
    the methods defined in alerter.py. I use fake inputs and analyse either the 
    outputs or the attributes.
    """
    
    # LogReader module is necessary for the alerter to work as it need its fictional time
    log_reader = LogReader()
    log_reader.fictional_time = datetime(2010,8,13,22,10,12)
    alerter = log_reader.statistics_manager.alerter
    
    # fake data stored in testdata.py
    section_metrics = test_alerter_data['section_metrics']
    metrics_to_push = test_alerter_data['sections_metrics_to_push']
    
    def test_remove_outdated_metrics(self):
        """ Check if the outdated metrics are removed """
        
        self.alerter.section_metrics_batch = self.section_metrics
        self.alerter._remove_outdated_metrics()
        assert len(self.alerter.section_metrics_batch['api']) == 3
        assert len(self.alerter.section_metrics_batch['report']) == 4
    
    def test_is_high(self):
        """ Check if the flags are triggered, the average metrics hits of user
        is within the 5% range around the threshold """
        
        self.alerter.section_metrics_batch = self.section_metrics
        assert self.alerter._is_high('api') == True
        assert self.alerter._is_high('report') == False
        assert self.alerter._is_high('user') == False
    
    def test_is_normal(self):
        """ Check if the flags are triggered, the average metrics hits of user
        is within the 5% range around the threshold """
        
        self.alerter.section_metrics_batch = self.section_metrics
        assert self.alerter._is_normal('api') == False
        assert self.alerter._is_normal('report') == True
        assert self.alerter._is_normal('user') == False
    
    def test_push_metrics_should_raise_alert(self):
        """ Check the raise alert logic """
        
        self.alerter.section_metrics_batch = self.section_metrics
        self.alerter.sections_on_alert = {'api': False}
        self.alerter.push_metrics(self.metrics_to_push)
        assert self.alerter.sections_on_alert['api'] == True
    
    def test_push_metrics_should_drop_alert(self):
        """ Check the drop alert logic """
        
        self.alerter.section_metrics_batch = self.section_metrics
        self.alerter.sections_on_alert = {'report': True}
        self.alerter.push_metrics(self.metrics_to_push)
        assert self.alerter.sections_on_alert['report'] == False
    
    def test_push_metrics_should_not_trigger(self):
        """ Check that it doesn't trigger the alerts when it is not necessary """
        
        self.alerter.section_metrics_batch = self.section_metrics
        self.alerter.sections_on_alert = {'user': True}
        self.alerter.push_metrics(self.metrics_to_push)
        assert self.alerter.sections_on_alert['user'] == True
        
        self.alerter.section_metrics_batch = self.section_metrics
        self.alerter.sections_on_alert = {'user': False}
        self.alerter.push_metrics(self.metrics_to_push)
        assert self.alerter.sections_on_alert['user'] == False
