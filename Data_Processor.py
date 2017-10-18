from DataParser import DataParser
from CronsDataStructure import DataExplorer

data_obj = DataParser()
data_obj.fetch_cron_data()
data = data_obj.get_cron_data()

for node in data:
    if node != 'slave_b':
        break
    dex = DataExplorer(node_name=node,
                       cron_data=data[node]['cron_data'],
                       duration_data=data[node]['duration'])
    dex.populate_schedule_table()
    sched_data = dex.get_schedule_data()
