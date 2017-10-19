import pickle
import sys
from DataParser import DataParser
from CronsDataStructure import DataExplorer

class Recommender():
    scale = 5
    num_elements = 24 * (60 / scale)
    def __init__(self,cron='',duration=0):
        self.picklefile = "C:\\mydata\\Bits\\Courses\\4thSem\\Dissertation\\repository\\data.pickle"
        handle = open(self.picklefile,'rb')
        self.schedule_data   = pickle.load(handle)
        self.cron = cron
        self.duration = duration
        self.input_data = self.parse_cron_data()
        
    def get_recommendation(self,cron,duration):
        
        pass

    def parse_cron_data(self):
        cron = self.cron        
        cron_data = {}
        attributes = cron.split(' ')
        mins_id = attributes[0]
        time_id = attributes[1]
        week_id = attributes[4]

        wkid,time_list = self.expand_elements(week=week_id,time=time_id,minutes=mins_id)
        for wid in wkid:
            if wid in cron_data.keys():
                cron_data[wid] += time_list            
            else:
                cron_data[wid] = time_list
        return cron_data
    def expand_elements(self,week = '',time='',minutes=''):
        week_ids = self.get_range_values(week,isWeek=True)
        time_ids = self.get_range_values(time)
        minute_ids = self.get_range_values(minutes,isMins=True)
        time_list = []
        wids = []
        weeks = {}     
        for mid in minute_ids:         
            for tid in time_ids:             
                time_list.append(str(tid)+':'+str(mid))     
        for wid in week_ids:
            weeks[wid] = time_list
            wids.append(str(wid))
        return wids,time_list    
        

    def get_range_values(self,value,isMins=False,isWeek=False):
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
            elif (value == '*') and isWeek:
                returnvalues+=range(0,7)
            else:
                returnvalues.append(value)
        return returnvalues

    def get_boundary_times(self,cronstring='',duration=0):
        scale = 5
        value_hour = int(cronstring.split(':')[0])
        value_min = int(cronstring.split(':')[1])
        start = (value_hour * (60/scale)) +(int(value_min)/scale)
        end   = start + (duration/scale)
        return start, end    

    def check_if_slots_available(self):
        num_elements = Recommender.num_elements
        scale        = Recommender.scale
        parsed_input = self.input_data
        parsed_input_boundary = {}
        for week in parsed_input:
            parsed_input_boundary[week] = []
            for element in parsed_input[week]:
                start,end = self.get_boundary_times(cronstring=element,duration=self.duration)
                parsed_input_boundary[week].append({'start':start,'end':end})
        isavailable = True

        for node in self.schedule_data:
            isavailable = True
            for week_id in parsed_input_boundary:
                for time_element in parsed_input_boundary[week_id]:
                    start_index = time_element['start']
                    end_index   = time_element['end']
                    if end_index < num_elements:
                        isavailable = isavailable and self.isAvailable(searchlist=self.schedule_data[node][week_id],start=start_index,end=end_index)
                    else:
                        isavailable = isavailable and self.isAvailable(searchlist=self.schedule_data[node][week_id],start=start_index,end=num_elements)
                        newstart  = 0
                        newend    = end_index - num_elements
                        newweek_id = str((int(week_id) + 1) % 7)
                        isavailable = isavailable and self.isAvailable(searchlist=self.schedule_data[node][newweek_id],start=newstart,end=newend)                        
            if isavailable:
                return node
                        
        
                    
    def isAvailable(self,searchlist=[],start=0,end=0):
        found = True
        for index in range(start,end):
            if searchlist[index] == '0':
                found = found and True
            else:
                found = found and False
        return found
        


cron_string = sys.argv[1]
duration    = sys.argv[2]
#cron_string = "30 18 * * 1"
#duration    = 360
r = Recommender(cron_string,int(duration))
slave_available = r.check_if_slots_available()

print "\n\n*****************************"
print "******* RECOMMENDATION ******"
print "*****************************"
if slave_available:
    print "NODE AVAILABLE - \"%s\"" %(slave_available)
else:
    print "NO Slave nodes available for the input cron.\nConsider Cloning a new VM"
print "\n\n\n"
