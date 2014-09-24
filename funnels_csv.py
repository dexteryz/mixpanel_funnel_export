#! /usr/bin/env python
#
# Export Mixpanel funnel start and completion data to CSV
# Author: Dexter Zhuang

import time
import csv
from client import Mixpanel
try:
    import json
except ImportError:
    import simplejson as json
    
# connect with the API through client library with API key 

api = Mixpanel(
	api_key = 'XXXXXXXXXXXXXXXXXXXXXX', 
	api_secret = 'XXXXXXXXXXXXXXXXXXXXXX'
)

# open csv file
f = csv.writer(open("mixpanel_funnels.csv", "wb+"))

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

    total_output = []
    
    # request funnel 1 data
    funnel_one = funnel_request(111111, from_date, to_date, funnel_length, funnel_interval)
    total_output = [list(x) for x in zip(*funnel_one)]
    
    # request funnel 2 data
    funnel_two = funnel_request(222222, from_date, to_date, funnel_length, funnel_interval)
    for col in ([list(x) for x in zip(*funnel_two)]):
        total_output.append(col)

    # reformat funnel output into transposed view
    final_output = [list(x) for x in zip(*total_output)]
    
    # create headers
    header = ["Date", "Funnel 1 Var 1", "Funnel 1 Var 2", 
                "Date", "Funnel 2 Var 1", "Funnel 2 Var 2",
                ]
    
    # write headers to csv
    f.writerow(header)
    
    # write reformmated output into csv
    f.writerows(final_output)
