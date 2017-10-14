from random import randint
cron_data = {'1':['22:30','23:30'],
             '2':['22:30','23:30'],
             '2':['22:30','23:30'],
             '*':['01:00','02:00','04:00','08:00']}

map_week = {}
duration = 30
scale = 5
num_elements = 24*(60/scale)
map_day = ['0']*num_elements

def IsAvailable(data,start,end,week_id):
    traversed = {}
    sched_ids = []
    sched_id_dict = {}
    for i in range(start,end):
        if data[i] != '0':            
            if data[i].__contains__(','):
                sched_ids = data[i].split(',')
                for element in sched_ids:
                    sched_id_dict[element] = ''
            else:
                sched_id_dict[data[i]] = ''
                
    for schedule_id in sched_id_dict:
        #print map_week[schedule]
        print "SCHEDULE ID",schedule_id
        print "WEEK ID",week_id
        print map_week[schedule_id][int(week_id)]
        

for cron in cron_data:
    cron_prefix = 'c' + str(randint(1,999))
    week_schedule = [0,0,0,0,0,0,0]
    value = cron_data[cron]

    for index in range(0,len(value)):
        value_hour = int(value[index].split(':')[0])
        value_min  = int(value[index].split(':')[1])
        start = (value_hour * (60/scale)) +(int(value_min)/scale)
        end   = start + (duration/scale)
        IsAvailable(map_day,start,end,cron)
        if end > num_elements:
            for i in range(start,num_elements):
                if map_day[i] == '0':
                    map_day[i] = cron_prefix
            for j in range(0,end-num_elements):
                if map_day[j] == '0':
                    map_day[j] = "!"+cron_prefix
        else:        
            for i in range(start,end):
                if map_day[i] == '0':
                    map_day[i] = cron_prefix                
        
    if cron == '*':
        week_schedule[0:7] = [1] * 6
    else:        
        week_schedule[int(cron)] = 1
    map_week[cron_prefix] = week_schedule
    week_schedule=[]
   
start = 0
durn = (60/scale)
for i in range(0,len(map_day)/durn):
    end = start + durn
    print i,"=>",map_day[start:end]
    start = end        

print "\n",map_week

def IsAvailable(data,start,end,week_id):
    traversed = {}
    for i in range(start,end):
        if data[i] != '0':
            if data[i].__contains__(','):
                return True
            
    return
    
