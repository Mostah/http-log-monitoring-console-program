"""
front.console_GUI

This module manages the application GUI and keep it updated in realtime.
"""

import npyscreen
from datetime import datetime

class ConsoleGUI(npyscreen.NPSApp):
    """
    The class use to render the application in the user console
    """

    def __init__(self, alert_threshold, alert_window):
        # npyscreen form widget, parent of all widgets in GUI
        self.window = None
        
        # different data values to show in GUI
        self.general_information = None
        self.traffic_information = None
        self.sections_stats_grid = None
        self.alert_history_grid = None
        
        # values for the general information frame
        self.alert_threshold = alert_threshold
        self.alert_window = alert_window
        self.begining_time = datetime.utcnow()

    def while_waiting(self):
        """ defines the default actions to be performed while waiting for user
        here this function updates widget data values periodically
        """

        # updating data values for all section
        self.general_information.values = ['','Description: If no timeframe is mentioned, stats ','are calculated over a 60min timeframe.',
                                           '','Time monitoring:      00:12:24', 'Alert Threshold:      10s', 
                                           'Alert Window:         120s', '', '', 'Press enter or ctrl-c to quit']
        self.traffic_information.values = ['', 'Hits (10s):         13/s', '', 'Mininimum:          2/s', 
                                        'Average:            14/s', 'Maximum:            25/s', '', 
                                           'Availability:       0.89', 'Unique hosts:       16', 'Total Bytes:        62KB' ]
        self.sections_stats_grid.values = [
            ['api','24/s','25/s','21/s','6','22KB','0.7','200: 24, 401: 2, 500: 3'],
            ['api','24/s','25/s','21/s','6','22KB','0.8','200: 24, 401: 2, 500: 3'],
            ['api','24/s','25/s','21/s','6','22KB','0.85','200: 24, 401: 2, 500: 3'],
            ['api','24/s','25/s','21/s','6','22KB','0.9','200: 24, 401: 2, 500: 3'],
            ['api','24/s','25/s','21/s','6','22KB','0.95','200: 24, 401: 2, 500: 3'],
            ['api','24/s','25/s','21/s','6','22KB','0.99','200: 24, 401: 2, 500: 3'],
        ]
        self.alert_history_grid.values = [
            ['High traffic on section : api','2019-10-29 11:12:36', '87/s'],
            ['High traffic on section : api','2019-10-29 11:12:36', '87/s'],
            ['Back to normal on section : api', '2019-10-29 11:12:36', '12/s']
        ]


        # display updated values in widgets, call 'Widget.display()' method
        self.general_information.display()
        self.traffic_information.display()
        self.sections_stats_grid.display()
        self.alert_history_grid.display()
        
    def main(self):
        """ 'main' function of npyscreen.NPSApp application object
        this function help in initial widget setup and rendering
        """

        # time(100ms) to wait before rerendering
        self.keypress_timeout_default = 10

        # Form widget instance
        self.window = WindowForm(parentApp=self, name="HTTP Log Monitor",)

        # setup a section for General Information
        self.general_information = self.window.add(npyscreen.BoxTitle, name="General Information", max_height=14, max_width=75, relx=2, rely=2)
        self.general_information.editable = False
        self.general_information.entry_widget.scroll_exit = True
        self.general_information.values = []

        # setup a section for Traffic Information
        self.traffic_information = self.window.add(npyscreen.BoxTitle, name="General Traffic Information", max_height=14, max_width=75, relx=77, rely=2)
        self.traffic_information.editable = False
        self.traffic_information.entry_widget.scroll_exit = True
        self.traffic_information.values = []
        
        # setup a section for Sections stats
        self.sections_stats_title = self.window.add(npyscreen.TitleText, name='Most Visited Sections', relx=2, rely=18)
        self.sections_stats_title.editable = False
        self.sections_stats_grid = self.window.add(StatGrid, max_height=12, column_width=20, relx=2, rely=20, 
                                                   col_titles=['Sections','Hits (10s)','Avg hits (10min)','Avg hits (60min)','Unique hosts','Total Bytes','Availability','Codes count'] )
        self.sections_stats_grid.editable = False
        self.sections_stats_grid.values = []

        # setup a section for Alert history
        self.alerts_title_title = self.window.add(npyscreen.TitleText, name='Alert History', relx=2, rely=35)
        self.alerts_title_title.editable = False
        self.alert_history_grid = self.window.add(AlertGrid, max_height=11, column_width=35, relx=2,rely=37, max_width=115,
                                                  col_titles=['Info','Time','Hits'])
        self.alert_history_grid.editable = False
        self.alert_history_grid.values = []

        # update parent widget by embedding sub-widgets
        self.window.edit()
        
        
class WindowForm(npyscreen.ActionForm):

    def create(self, *args, **keywords):
        super(WindowForm, self).create(*args, **keywords)
    
    def while_waiting(self):
        pass
    
class AlertGrid(npyscreen.GridColTitles):
    # You need to override custom_print_cell to manipulate how
    # a cell is printed. In this example we change the color of the
    # text depending on the string value of cell.
    def custom_print_cell(self, actual_cell, cell_display_value):
        if 'High' in cell_display_value:
            actual_cell.color = 'DANGER'
        elif 'Back' in cell_display_value:
            actual_cell.color = 'SAFE'
        else:
            actual_cell.color = 'CAUTION'
            
class StatGrid(npyscreen.GridColTitles):

    def custom_print_cell(self, actual_cell, cell_display_value):
        if cell_display_value <= '0.8':
            actual_cell.color = 'DANGER'
        elif cell_display_value <= '0.9':
            actual_cell.color = 'CAUTION'
        elif cell_display_value < '1.0':
            actual_cell.color = 'SAFE'
        else:
            actual_cell.color = 'STANDOUT'