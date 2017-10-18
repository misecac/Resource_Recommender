from random import randint

class DataExplorer():
    scale = 5
    num_elements = 24 * (60 / scale)
    
    def __init__(self,node_name,cron_data,duration_data):
        self.cron_data = cron_data
        self.duration  = duration_data
        self.node_name = node_name
        self.map_day   = ['0'] * DataExplorer.num_elements
        self.schedule_dict = {}
        self.generate_schedule_table()

    def generate_schedule_table(self):
        for week_id in range(0,7):            
            self.schedule_dict[str(week_id)] = ['0'] * DataExplorer.num_elements
        
    def populate_schedule_table(self):
        start = 0
        end   = 0
        for week in self.cron_data:
            value = self.cron_data[week]
            week_index = week
            if week != '*':                
                for index in range(0,len(value)):
                    cron_prefix = 'c'+str(randint(1,1000))
                    start,end = self.get_boundary_times(cronstring=self.cron_data[week_index][index],duration=self.duration[week_index][index])
                    if end <= DataExplorer.num_elements:                        
                        self.fill_hour_data(start,end,cron_prefix,week_index,self.schedule_dict[week_index])
                    else:
                        self.fill_hour_data(start,DataExplorer.num_elements,cron_prefix,week_index,self.schedule_dict[week_index])
                        new_week_index = str((int(week_index)+1) % 7)
                        new_end = end-DataExplorer.num_elements
                        self.fill_hour_data(0,new_end,cron_prefix,new_week_index,self.schedule_dict[new_week_index])
                    
            else:
                for index in range(0,len(value)):
                    cron_prefix = 'c'+str(randint(1,1000))
                    start,end = self.get_boundary_times(cronstring=self.cron_data['*'][index],duration=self.duration['*'][index])
                    for week_index in range(0,7):
                        week_index  = str(week_index)
                        if end <= DataExplorer.num_elements:
                            self.fill_hour_data(start,end,cron_prefix,week_index,self.schedule_dict[week_index])
                        else:                            
                            self.fill_hour_data(start,DataExplorer.num_elements,cron_prefix,week_index,self.schedule_dict[week_index])
                            new_week_index = str((int(week_index)+1) % 7)
                            new_end = end-DataExplorer.num_elements
                            self.fill_hour_data(0,new_end,cron_prefix,new_week_index,self.schedule_dict[new_week_index])
            
    def get_boundary_times(self,cronstring='',duration=0):
        scale = DataExplorer.scale
        value_hour = int(cronstring.split(':')[0])
        value_min = int(cronstring.split(':')[1])
        start = (value_hour * (60/scale)) +(int(value_min)/scale)
        end   = start + (duration/scale)
        return start, end    
        
    def fill_hour_data(self,start,end,cron_prefix,week_id,map_day):
        num_elements = DataExplorer.num_elements
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
        self.schedule_dict[week_id] = map_day
        
    def get_schedule_data(self):
        return self.schedule_dict

    def Print_Data(self,schedule_data):
        start = 0
        scale = DataExplorer.scale
        durn = (60 / scale)
    
        for i in range(0,len(schedule_data)/durn):
            end = start + durn
            print i,"=>",schedule_data[start:end]
            start = end        
             

def Main():
    cron_data_1 = {'*':['23:00','13:30']}
    duration_data_1 = {'*':[3*60,30]}
    dex1 = DataExplorer(node_name="NodeA",cron_data=cron_data_1,duration_data=duration_data_1)
    dex1.populate_schedule_table()
    sched_data = dex1.get_schedule_data()
    dex1.Print_Data(sched_data['0'])
    dex1.Print_Data(sched_data['2'])    

Main()
