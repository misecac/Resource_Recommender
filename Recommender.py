import pickle
import sys
from DataParser import DataParser
from CronsDataStructure import DataExplorer

class Stack:    
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek_stack_top(self):         
         if len(self.items) > 0:
             return self.items[len(self.items)-1]
         else:
             return False
            
     def peek_stack_bottom(self):
         return self.items[0]
         
         
     def printstack(self):
        print self.items

     def size(self):
         return len(self.items)

class Recommender():
    scale = 5
    recommendations_count = 3
    num_elements = 24 * (60 / scale)
    def __init__(self,cron='',duration=0):
        self.picklefile = "C:\\mydata\\Bits\\Courses\\4thSem\\Dissertation\\repository\\data.pickle"
        handle = open(self.picklefile,'rb')
        self.schedule_data   = pickle.load(handle)
        self.cron = cron
        self.duration = duration
        self.input_data = self.parse_cron_data()
        self.recommendations = {}
        
    """
    Desc : Generating the recommendation times for the given input duration
    """
    def get_recommendations(self):
        cron = self.cron
        availability = {}
        duration = self.duration
        weekids = self.input_data.keys()
        slaveids = self.schedule_data.keys()
        self.recommendations[slaveids[0]] = {}
        for slave in self.schedule_data:
             availability = self.search_in_week(weekids,self.schedule_data[slave])
             self.recommendations[slave] = availability

        for recommendation in self.recommendations:
             print recommendation,self.recommendations[recommendation]
        
    
    def get_no_of_slots(self,duration=0):
        if duration > 0 and duration%Recommender.scale == 0:             
            return (duration / 5)
          
    def search_in_week(self,weekids,data):        
        week_availability = {}
        available_list = []
        for week_id in weekids:            
            week_availability[week_id] = []
            week_availability[week_id] = self.scan_empty_slots(data[week_id])
        
        for key in week_availability:            
            if len(available_list) == 0:
                available_list = week_availability[key]            
            available_list = set(week_availability[key]).intersection(set(available_list))
        week_availability = self.get_available_blocks(available=available_list)
        return week_availability
            

    def convert_index_to_time(self,indexvalue=0):
        returnvalue = ''
        temp = indexvalue * 5
        returnvalue = str(temp/60) + ":" + str(temp%60)
        return returnvalue
        
    def get_available_blocks(self,available=[]):        
        available_blocks = []
        available = list(available)
        available.sort()
        s = Stack()
        newS = ''
        counter = 0
        for item in available:
            counter += 1
            v = s.peek_stack_top()
            if v == item-1:
                s.push(item)                
                if counter == len(available):                    
                    available_blocks.append(self.get_block_boundary_indices(stack_ref = s))
            else:                
                if s.size() > 0:
                    available_blocks.append(self.get_block_boundary_indices(stack_ref = s))
                else:
                    s.push(item)                    
                
        return available_blocks

    def get_block_boundary_indices(self,stack_ref = [],item=0):
        returnvalue = {'From':'','To':''}
        newS = Stack()
        while not stack_ref.isEmpty():
            newS.push(stack_ref.pop())        
        #stack_ref.push(item)
        returnvalue['From'] = self.convert_index_to_time(indexvalue=newS.peek_stack_top())
        returnvalue['To']   = self.convert_index_to_time(indexvalue=newS.peek_stack_bottom())
        return returnvalue
    
        
    def convert_index_to_times(self, available):
        available = list(available)
        available.sort()
        available_times = []
        temp = 0
    
        for index in available:
            temp = index * 5
            available_times.append(str(temp/60) + ":" + str(temp%60))

        for time in available_times:            
            pass
                       
    def scan_empty_slots(self,data):         
        avail_indices_week = []
        num_of_slots = self.get_no_of_slots(self.duration)
        for index in range(0,len(data)-num_of_slots+1):
            if data[index] == '0':
                if self.check_if_block_empty(data[index:(index+num_of_slots)],index,num_of_slots):                    
                    avail_indices_week.append(index)
        return avail_indices_week

    def check_if_block_empty(self,array,index,no_of_slots):
         
        counter = 0        
        for element in array:
            if element == '0':
                counter += 1
        if counter ==  no_of_slots:            
            return True
        else:             
             return False

    """
    Function parse_cron_data
    Desc     Parsing the input cron to generate times in hour:min format
    """
    
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

    """
    Function expand_elements
    Desc     Substituting the cron elements and generating multiple crons for the wildcards,
            For Ex: 4 crons will be generated from crons containing 9-12 in their elements
    """
    
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

    """
    Function  get_range_values
    Desc      Utility function to expand the cron element values containing - and ,
    """

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

    """
    Function get_boundary_times
    Desc     Getting the start and end of the 5-min blocks from the input cronstring
    """

    def get_boundary_times(self,cronstring='',duration=0):
        scale = 5
        value_hour = self.get_absolute_values(cronstring.split(':')[0])
        value_min  = self.get_absolute_values(cronstring.split(':')[1])        
        start = (value_hour * (60/scale)) +(int(value_min)/scale)
        end   = start + (duration/scale)
        return start, end

    def get_absolute_values(self,value):
        if value == '*' or value == 'H':
            value = 0
        else:
            value = int(value)
        return value

    """
    Function check_if_slots_available
    Desc     Main logic to search the if any resource is available during the requested time slot
    """

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
        

recommender_mode = sys.argv[1]
cron_string = sys.argv[2]
duration    = sys.argv[3]

r = Recommender(cron_string,int(duration))

if recommender_mode.lower()=="multiple":
     r.get_recommendations()
     exit
else:
     slave_available = r.check_if_slots_available()
     print "\n\n*****************************"
     print "******* RECOMMENDATION ******"
     print "*****************************"
     if slave_available:
         print "NODE AVAILABLE - \"%s\"" %(slave_available)
     else:
         print "NO Slave nodes available for the input cron.\nConsider Cloning a new VM"
     print "\n\n\n"
