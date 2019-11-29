
"""
front.service

This module fetch and transform the data to be ready to display.
"""

import random
from datetime import datetime

class Service:
    """
    A module made to fetch the data from the API and transform it to be ready to display.
    
    Attributes
    ----------
    alert_threshold : int
        threshold from which an alert is triggered
    alert_window : int
        time (in seconds) over which is calculated the average hits for the alert
    begining_time : datetime
        time of the instanciation of this module
    
    Methods
    -------
    get_general_information()
        get general information about this monitoring session
        
    get_traffic_information()
        get stats computed from the selected website
        
    get_sections_stats()
        get stats computed over all section
        
    get_alert_history()
        get history alert from all section
    
    """
    
    def __init__(self, alert_threshold, alert_window):
        """
        Parameters
        ----------
        alert_threshold : int
            threshold from which an alert is triggered
        alert_window : int
            time (in seconds) over which is calculated the average hits for the alert
        """
        
        self.alert_threshold = alert_threshold
        self.alert_window = alert_window
        self.begining_time = datetime.utcnow()
    
    def get_general_information(self):
        """get general information about this monitoring session
        """
        
        # computing the time since the begining of the monitoring session
        now = datetime.utcnow()
        time_monitoring = now - self.begining_time
        
        data = ['',
                'Description: If no timeframe is mentioned, stats are',
                'calculated over a 10 minutes timeframe.',
                '',
                'Time monitoring:      '+str(time_monitoring)[:-7], 
                'Alert Threshold:      '+str(self.alert_threshold)+'s', 
                'Alert Window:         '+str(self.alert_window)+'s', 
                '', 
                '', 
                'Press enter or ctrl-c to quit']
        return data

    def get_traffic_information(self):
        """get stats computed from the selected website
        """
        
        data = ['',
                'Hits (10s):         '+str(random.choice([8,9,10,11,12]))+'/s',
                '',
                'Mininimum:          '+str(random.choice([8,9,10,11,12]))+'/s',
                'Average:            '+str(random.choice([8,9,10,11,12]))+'/s',
                'Maximum:            '+str(random.choice([8,9,10,11,12]))+'/s',
                '',
                'Availability:       '+str(random.choice([0.89,0.91,0.92,0.93,0.94])),
                'Unique hosts:       '+str(random.choice([8,9,10,11,12])),
                'Total Bytes:        '+str(random.choice([8,9,10,11,12]))+'KB' ]
        return data
    
    def get_sections_stats(self):
        """get stats computed over all section
        """
        
        data = [
            ['api',str(random.choice([8,9,10,11,12]))+'/s',str(random.choice([8,9,10,11,12]))+'/s',str(random.choice([8,9,10,11,12]))+'/s','6','22KB','0.7','200: 24, 401: 2, 500: 3'],
            ['other',str(random.choice([8,9,10,11,12]))+'/s',str(random.choice([8,9,10,11,12]))+'/s',str(random.choice([8,9,10,11,12]))+'/s','6','22KB','0.7','200: 24, 401: 2, 500: 3'],
        ]
        return data
    
    def get_alert_history(self):
        """get history alert from all section
        """
        
        data = [
            ['High traffic on section : api','2019-10-29 11:12:36', '87/s'],
            ['High traffic on section : api','2019-10-29 11:12:36', '87/s'],
            ['Back to normal on section : api', '2019-10-29 11:12:36', '12/s']
        ]
        return data
    