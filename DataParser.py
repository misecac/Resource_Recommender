import os
import re

config_files_list = "C:\\Users\\ArunKumar_M\\.jenkins\\jobs\\configfiles"
config_fh = open(config_files_list,"r")

Data = {}
Data_Parsed = {}
slave_regex = "<assignedNode>(.*?)</assignedNode>"
cron_regex = "<spec>(.*?)</spec>"

def fetch_cron_data():
    for configfile in config_fh.readlines():
        slave_name = ''
        crons      = []
        
        configfile = configfile.strip("\n")

        fh = open(configfile,'r')
        content = fh.read()

        slave_searchObj = re.search(slave_regex,content)
        cron_searchObj = re.search(cron_regex,content,re.S)
        
        if slave_searchObj is not None:
            slave_name = slave_searchObj.group(1)
            slave_name = slave_name.strip("")
            
        if cron_searchObj is not None:
            crons       = cron_searchObj.group(1)
        
        if slave_name != '' and crons != '':
            newcron = crons.split("\n")        
            if slave_name not in Data.keys():
                Data[slave_name] = newcron            
            else:            
                Data[slave_name] = Data[slave_name]+newcron

def parse_cron_data():
    for node in Data:
        for cron in Data[node]:
            attributes = cron.split(' ')            
            mins_id = attributes[0]
            time_id  = attributes[1]
            week_id = attributes[4]
            expand_elements(week=week_id,time=time_id,minutes=mins_id)
            print week_id,mins_id,time_id
            
def expand_elements(week = '',time='',minutes=''):
     pass

def get_range_values(value):
    start = 0
    end = 0
    returnvalues = []
    if value.__contains__('-'):
        start = int(value.split('-')[0])
        end   = int(value.split('-')[1])
        for index in range(start,end):
            returnvalues.append(index)
    if value.__contains__(','):
        returnvalues = value.split(',')
    print returnvalues
    

get_range_values('10-15')
get_range_values('2,6')
#fetch_cron_data()
#parse_cron_data()
