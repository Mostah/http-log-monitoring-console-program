import sys
import signal
import argparse
from multiprocessing import Process

from front.console_GUI import ConsoleGUI
from back.log_pipeline.log_reader import LogReader

# in order to handle ctrl-c as try - except doesn't work well with multiprocessing
def signal_handle(_signal, frame):
    sys.exit()
    
if __name__ == '__main__':
    # initiating our ctrl-c catcher
    signal.signal(signal.SIGINT, signal_handle)
    
    # argument parser that get access to the argument given when running the program in the shell
    parser = argparse.ArgumentParser(description='Launch the GUI of the HTTP LOG MONITORING app')
    parser.add_argument('--f', metavar='file', type=str, default='back/logs/sample_csv.txt', required=False,
                    help='location of the logfile the app will run on')
    parser.add_argument('--thd', metavar='alert_threshold', type=int, default=10, required=False,
                    help='threshold upon which alerts are triggered')
    parser.add_argument('--wd', metavar='alert_window', type=int, default=120, required=False,
                    help='time windows over which stats are computed for the alerting system')
    parser.add_argument('--tf', metavar='timeframe', type=int, default=10, required=False,
                    help='timeframe over which all the stats are computed')

    # args given by the user
    args = parser.parse_args()

    # initiating the front and back processes
    log_reader = LogReader(args.tf, args.wd, args.thd, args.f)
    console_gui = ConsoleGUI(args.thd, args.wd, args.tf)
    
    # start the multiprocessing pool
    back_process = Process(target=log_reader.start_reading)
    back_process.start()
    front_process = Process(target=console_gui.run)
    front_process.start()
    




