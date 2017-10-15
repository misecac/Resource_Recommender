from random import randint

class DataExplorer():
    scale = 5
    num_elements = 24*(60/scale)
    def __init__(self,cron_dict,duration):
        self.cron_data = cron_dict
        self.duration = duration

    def IsAvailable(self,data_day,data_week,start,end,week_id):
        traversed = {}
        sched_ids = []
        sched_id_dict = {}
        result = True
        for i in range(start,end):
            if data_day[i] != '0':            
                if data_day[i].__contains__(','):
                    sched_ids = data_day[i].split(',')
                    for element in sched_ids:
                        if element.__contains__('!'):
                            element = element.replace('!','')
                        sched_id_dict[element] = ''
                else:
                    sched_id = data_day[i]
                    if sched_id.__contains__('!'):
                        sched_id = sched_id.replace('!','')
                    sched_id_dict[sched_id] = ''

        for schedule_id in sched_id_dict:
            if week_id == '*':
                for index in range(0,7):                
                    result = result and not data_week[schedule_id][index]
            else:
                result = result and not data_week[schedule_id][int(week_id)]        
        return result

    def IsScheduleAvailable(self,data_day=[],data_week={},week_id='',cronlist=[],duration=0):
        newend = 0    
        result = True
        end = 0
        num_elements = DataExplorer.num_elements
        for index in cronlist:
            start,end = self.get_boundary_times(index,duration)
            if end > num_elements:
                newend = end - num_elements
                end = num_elements
                result = result and self.IsAvailable(data_day,data_week,0,newend,week_id)
                result = result and self.IsAvailable(data_day,data_week,start,end,week_id)
            else:
                result = result and self.IsAvailable(data_day,data_week,start,end,week_id)
            
        return result

    def get_boundary_times(self,cronstring='',duration=0):
        scale = DataExplorer.scale
        value_hour = int(cronstring.split(':')[0])
        value_min = int(cronstring.split(':')[1])
        start = (value_hour * (60/scale)) +(int(value_min)/scale)
        end   = start + (duration/scale)
        return start, end
    
    def generate_schedule_table(self,cron_data={},duration=0,map_day=['0']*num_elements,map_week={}):
        num_elements = DataExplorer.num_elements
        for cron in cron_data:        
            cron_prefix = 'c' + str(randint(1,999))
            week_schedule = [0,0,0,0,0,0,0]
            value = cron_data[cron]
            if not self.IsScheduleAvailable(cronlist=cron_data[cron],duration=duration,data_day=map_day,data_week=map_week, week_id=cron):
                print cron_data[cron]
                print 'unavailable'
                break
            
            for index in range(0,len(value)):            
                start,end = self.get_boundary_times(value[index],duration)
                #isAvailable = IsAvailable(map_day,map_week,start,end,cron)
                    
                if end > num_elements:
                    for i in range(start,num_elements):
                        if map_day[i] == '0':
                            map_day[i] = cron_prefix
                        else:
                            map_day[i] += ","+cron_prefix
                    for j in range(0,end-num_elements):
                        if map_day[j] == '0':
                            map_day[j] = "!"+cron_prefix
                        else:
                            map_day[j] += ",!"+cron_prefix
                else:        
                    for i in range(start,end):
                        if map_day[i] == '0':
                            map_day[i] = cron_prefix
                        else:
                            map_day[i] += ","+cron_prefix                
                
            if cron == '*':
                week_schedule[0:7] = [1] * 6
            else:            
                week_schedule[int(cron)] = 1
            map_week[cron_prefix] = week_schedule
            week_schedule=[]
        return map_day,map_week
    
    def Print_Data(self,map_day,map_week): 
        start = 0
        scale = DataExplorer.scale
        durn = (60/scale)
        for i in range(0,len(map_day)/durn):
            end = start + durn
            print i,"=>",map_day[start:end]
            start = end        
        print "\n",map_week

def Main():
    cron_data_1 = {'1':['00:00']}
    duration_1 = 36*60
    cron_data_2 = {'2':['00:00']}
    duration_2 = 24*60
    dex1 = DataExplorer(cron_data_1,duration_1)
    map_day_updated,map_week_updated = dex1.generate_schedule_table(cron_data=cron_data_1,duration=duration_1)
    dex1.Print_Data(map_day_updated,map_week_updated)
    dex2 = DataExplorer(cron_data_2,duration_2)
    map_day_1,map_week_1 = dex2.generate_schedule_table(cron_data=cron_data_2,duration=duration_2)    
    dex2.Print_Data(map_day_1,map_week_1)

Main()    

