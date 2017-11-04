from data_explorer import DataExplorer
def Main():

    cron_data_1 = {'1':['00:00'],'2':['00:00']}
    duration_1 = 36*60
    
    dex1 = DataExplorer(node_name="NodeA",cron_data=cron_data_1,duration=duration_1)
    dex1.generate_schedule_table()
    schedule_table_1 = dex1.get_schedule_table()
    dex1.Print_Data(schedule_table_1)
    
    cron_data_2 = {'2':['00:00']}
    duration_2 = 24*60
    
    dex2 = DataExplorer(node_name="NodeB",cron_data=cron_data_2,duration=duration_2)
    dex2.generate_schedule_table()
    schedule_table_2 = dex2.get_schedule_table()
    dex2.Print_Data(schedule_table_2)
    
Main()
