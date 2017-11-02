import pickle
from DataParser import DataParser
from CronsDataStructure import DataExplorer

data_obj = DataParser()
data_obj.fetch_cron_data()
data = data_obj.get_cron_data()
DataSet = {}
for node in data:
    DataSet[node] = {}
    dex = DataExplorer(node_name=node,
                       cron_data=data[node]['cron_data'],
                       duration_data=data[node]['duration'])
    dex.populate_schedule_table()
    node_schedule_table = dex.get_schedule_data()
    DataSet[node] = node_schedule_table


with open("C:\\mydata\\Bits\\Courses\\4thSem\\Dissertation\\repository\\data.pickle",'wb') as f:
    pickle.dump(DataSet,f)
