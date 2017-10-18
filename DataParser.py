import os
import re
import requests
import json

class DataParser():
    slave_regex = "<assignedNode>(.*?)</assignedNode>"
    cron_regex = "<spec>(.*?)</spec>"
    url_template_duration = "http://localhost:8080/job/%JOB_NAME%/api/json?tree=builds[number,result,duration]"
    buffertime = 5
    def __init__(self):
        self.config_files_list = "C:\\Users\\ArunKumar_M\\.jenkins\\jobs\\configfiles"
        self.Data_Parsed = {}
        

    def fetch_duration_data(self,job_name):
        avg_duration_count = 5
        totalduration = 0
        buffertime = self.buffertime
        avg_duration = 0
        index = 0
        url = DataParser.url_template_duration
        url = url.replace('%JOB_NAME%',job_name)
        response = requests.get(url)
        
        if(response.ok):
            Data_Duration = json.loads(response.content)
            for key in Data_Duration['builds']:
                if (key['result']) == "SUCCESS":
                    index += 1
                    totalduration += key['duration']
                    if index > avg_duration_count:
                        break
            if avg_duration_count > index:
                avg_duration_count = index
            totalduration = totalduration / avg_duration_count
            totalduration = totalduration / 1000
            totalduration = totalduration/60
            totalduration = (totalduration-(totalduration%5)) + 5
            totalduration = totalduration + buffertime
            return totalduration
        
    def fetch_cron_data(self):
        Data = {}
        duration = 0
        config_fh = open(self.config_files_list,"r")
        for configfile in config_fh.readlines():
            slave_name = ''
            crons      = []
            job_name = os.path.basename(os.path.dirname(configfile))
            duration = self.fetch_duration_data(job_name)

            configfile = configfile.strip("\n")

            fh = open(configfile,'r')
            content = fh.read()
            fh.close()
            slave_searchObj = re.search(DataParser.slave_regex,content)
            cron_searchObj = re.search(DataParser.cron_regex,content,re.S)
            
            if slave_searchObj is not None:
                slave_name = slave_searchObj.group(1)
                slave_name = slave_name.strip("")
                
            if cron_searchObj is not None:
                crons       = cron_searchObj.group(1)
            
            if slave_name != '' and crons != '':
                newcron = crons.split("\n")        
                Data = newcron                
            self.parse_data(Data,slave_name,duration)
        

    def parse_data(self,Data,node,duration):
        if node not in self.Data_Parsed.keys():
            self.Data_Parsed[node] = {}
            self.Data_Parsed[node]['cron_data'] = {}
            self.Data_Parsed[node]['duration'] = {}

        for cron in Data:
            attributes = cron.split(' ')
            mins_id = attributes[0]
            time_id  = attributes[1]
            week_id = attributes[4]
            wid,time_list = self.expand_elements(week=week_id,time=time_id,minutes=mins_id)
            
            if wid in self.Data_Parsed[node]['cron_data'].keys():
                self.Data_Parsed[node]['cron_data'][wid] += time_list
                self.Data_Parsed[node]['duration'][wid] += [duration] * len(time_list)
            else:
                self.Data_Parsed[node]['cron_data'][wid] = time_list
                self.Data_Parsed[node]['duration'][wid] = [duration]*len(time_list)
    
    def expand_elements(self,week = '',time='',minutes=''):
         week_ids = self.get_range_values(week)
         time_ids = self.get_range_values(time)
         minute_ids = self.get_range_values(minutes,isMins=True)
         time_list = []
         weeks = {}     
         for mid in minute_ids:         
             for tid in time_ids:             
                 time_list.append(str(tid)+':'+str(mid))     
         for wid in week_ids:
             weeks[wid] = time_list
         return wid,time_list    
        

    def get_range_values(self,value,isMins=False):
        start = 0
        end = 0
        returnvalues = []
        if value.__contains__('-'):
            start = int(value.split('-')[0])
            end   = int(value.split('-')[1])
            for index in range(start,end):
                returnvalues.append(index)
        elif value.__contains__(','):
            returnvalues = value.split(',')
        else:
            if (value == 'H' or value == '*') and isMins:
                returnvalues.append('0')
            else:
                returnvalues.append(value)
        return returnvalues
    
    def get_cron_data(self):
        return self.Data_Parsed
