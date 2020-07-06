#!/Users/michaelcondon/anaconda3/bin/python3

import pandas as pd
import numpy as np
from csv import writer
import pyspeedtest
from datetime import datetime

def test_speedII():
    """
    Do a speedtest
    """
    speedtest = pyspeedtest.SpeedTest()
    now =datetime.now()
    resultsII = [round(speedtest.ping(),2),round(speedtest.download()/1000000,2),
        round(speedtest.upload()/1000000,2),now.strftime('%Y-%m-%d'),
        now.strftime("%H:%M:%S")]
    return resultsII

results = test_speedII()

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

append_list_as_row(r'/Users/michaelcondon/Documents/GitHub/Speedtest/speedtest_logs.csv',results)