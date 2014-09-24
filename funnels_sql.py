#! /usr/bin/env python
#
# Export Mixpanel funnel start and completion data to SQL DB
# Author: Dexter Zhuang

import time
import csv
from client import Mixpanel
try:
    import json
except ImportError:
    import simplejson as json
import sqlite3
    
# connect with the API through client library with API key 

api = Mixpanel(
	api_key = 'XXXXXXXXXXXXXXXXXXXXXX', 
	api_secret = 'XXXXXXXXXXXXXXXXXXXXXX'
)

# cconnect with the sql db
conn = sqlite3.connect('mixpanel_funnels.db')

# specify funnel parameters
today = time.strftime("%Y%m%d")
from_date = '2014-08-01'
to_date = '2014-08-31'
funnel_length = 1
funnel_interval = 1

# request the funnel data
# params: funnel ID, start date, end date, time window in days for completing the funnel, intervals in days, boolean for adding the date in the output)
# return: list of lists of funnel data
def funnel_request(funnel_id, start_date, end_date, length, interval, add_date=True):
    
    funnel_output = []
    
    data = api.request(['funnels'], {
    	'funnel_id': funnel_id,
    	'from_date' : start_date,
    	'to_date' : end_date,
        'length' : length,
    	'interval' : interval
    	})
    
    data = json.loads(data)
    
    if add_date:
        for date in data['data']:
            data_row = [date, data['data'][date]['analysis']['starting_amount'], data['data'][date]['analysis']['completion']]
            funnel_output.append(data_row)
    else:
        for date in data['data']:
            data_row = [data['data'][date]['analysis']['starting_amount'], data['data'][date]['analysis']['completion']]
            funnel_output.append(data_row)
    
    return funnel_output

if __name__ == '__main__':
    
    # create the cursor object
    c = conn.cursor()
    
    # initialize the tables
    total_output = []
    
    # drop table if it exists
    c.executescript('''DROP TABLE if exists funnel_one;
                        DROP TABLE if exists funnel_two;
                        ''')
    
    # write the headers to SQL DB
    c.executescript('''CREATE TABLE funnel_one (date text, var_one int, var_two int);
                        CREATE TABLE funnel_two (date text, var_one int, var_two int);
                        ''')

    # request funnel 1 data
    funnel_one = funnel_request(111111, from_date, to_date, funnel_length, funnel_interval)
    
    # request funnel 2 data
    funnel_two = funnel_request(222222, from_date, to_date, funnel_length, funnel_interval)

    # write the funnels data dump to the SQL DB
    for item in funnel_one:
        c.execute('INSERT INTO funnel_one VALUES (?,?,?)', item)
    
    for item in funnel_two:
        c.execute('INSERT INTO funnel_two VALUES (?,?,?)', item)
    
    conn.commit()