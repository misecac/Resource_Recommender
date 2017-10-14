from random import randint

scale = 5
num_elements = 24*(60/scale)

def IsAvailable(data_day,data_week,start,end,week_id):
    traversed = {}
    sched_ids = []
    sched_id_dict = {}
    result = True
    for i in range(start,end):
        if data_day[i] != '0':            
            if data_day[i].__contains__(','):
                sched_ids = data_day[i].split(',')
                for element in sched_ids:
                    sched_id_dict[element] = ''
            else:    
                sched_id_dict[data_day[i]] = ''

    for schedule_id in sched_id_dict:
        result = result and not data_week[schedule_id][int(week_id)]        
    return result
        
        
def generate_schedule_table(cron_data={},duration=0,map_day=['0']*num_elements,map_week={}):
    for cron in cron_data:        
        cron_prefix = 'c' + str(randint(1,999))
        week_schedule = [0,0,0,0,0,0,0]
        value = cron_data[cron]

        for index in range(0,len(value)):
            value_hour = int(value[index].split(':')[0])
            value_min  = int(value[index].split(':')[1])
            start = (value_hour * (60/scale)) +(int(value_min)/scale)
            end   = start + (duration/scale)
            isAvailable = IsAvailable(map_day,map_week,start,end,cron)
            if (not isAvailable):
                print "Cannot allocate", cron_data[cron]
                break
                
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
    
def Print_Data(map_day,map_week): 
    start = 0
    durn = (60/scale)
    for i in range(0,len(map_day)/durn):
        end = start + durn
        print i,"=>",map_day[start:end]
        start = end        
    print "\n",map_week

def Main():
    cron_data = {'1':['22:30','23:30'],
             '2':['22:30','23:30'],
             '*':['01:00','02:00','04:00','08:00']}
    duration = 30
    
    map_day_updated,map_week_updated = generate_schedule_table(cron_data=cron_data,duration=duration)
    Print_Data(map_day_updated,map_week_updated)

    cron_data = {'4':['23:00','22:30'],'3':['22:30']}
    duration = 30
    map_day_1,map_week_1 = generate_schedule_table(cron_data=cron_data,duration=duration)    
    Print_Data(map_day_1,map_week_1)

Main()    

