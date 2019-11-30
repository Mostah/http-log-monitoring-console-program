
"""
front.service

This module fetch and transform the data to be ready to display.
"""

import random
import requests
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
    timeframe : int
        timeframe selected by the user over which stats are computed
    
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
    
    API_URL = 'http://localhost:5000'
    
    def __init__(self, alert_threshold, alert_window, timeframe):
        """
        Parameters
        ----------
        alert_threshold : int
            threshold from which an alert is triggered
        alert_window : int
            time (in seconds) over which is calculated the average hits for the alert
        timeframe : int
            timeframe selected by the user over which stats are computed
        """
        self.TIMEFRAME = timeframe
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
                'calculated over the selected timeframe.',
                '',
                'Selected timeframe    '+str(self.TIMEFRAME)+'min',
                '',
                'Time monitoring:      '+str(time_monitoring)[:-7], 
                'Alert Threshold:      '+str(self.alert_threshold)+'s', 
                'Alert Window:         '+str(self.alert_window)+'s', 
                '', 
                'Press enter or ctrl-c to quit']
        return data

    def get_traffic_information(self):
        """get stats computed from the selected website
        """
        
        r = requests.get(self.API_URL+'/general-traffic/last').json()[0]
        data = ['',
                'Hits (10s):         '+str(r['hits'])+'/s',
                '',
                'Mininimum:          '+str(round(r['minimum'],2))+'/s',
                'Average:            '+str(round(r['average'],2))+'/s',
                'Maximum:            '+str(round(r['maximum'],2))+'/s',
                '',
                'Availability:       '+str(round(r['availability'],2)),
                'Unique hosts:       '+str(r['unique_hosts']),
                'Total Bytes:        '+str(r['total_bytes'])+'KB' ]
        
        return data
    
    def get_sections_stats(self):
        """get stats computed over all section
        """
        
        r = requests.get(self.API_URL+'/section-traffic/lasts').json()
        data = [[
            entry['section'],
            str(round(entry['hits'],2))+'/s',
            str(round(entry['average'],2))+'/s',
            entry['unique_hosts'],
            str(entry['total_bytes'])+'KB',
            round(entry['availability'],2),
            entry['error_codes_count']
        ] for entry in r]
        
        return data
    
    def get_alert_history(self):
        """get history alert from all section
        """
        
        r = requests.get(self.API_URL+'/alerts/history').json()
        
        data = [[
            entry['status']*'High traffic on : '+(1-entry['status'])* 'Back to normal on : '+ entry['section'],
            entry['time'],
            str(round(entry['hits'],2))+'/s']
            for entry in r]
 
        return data
    