#Script to collect data from an OPCUA Server by using the module filemanager.py

from settings  import Result_path, url, data_name, nID_HM_4 as root_ID
import os
import errno
from datetime import datetime
from file_manager import OPCUA_collector



Result_path = Result_path + "/Results" + datetime.now().strftime('_%Y-%m-%d_%H-%M-%S')      
try:            #Path + subfolder will be created, if path already exists, only new subfolder within path will be created
    os.makedirs(Result_path)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass


#csv specific settings
cols_vs_id = {"PDatTime" : "PDatTime","BASET": "BASET_2","CO2" : "CO2", "CO2_pressure" : "CO2_pressure"}       #
initial_row_filler = [["Value"], ["Unit"], []]      #every list in the list contains constant values to fill the rows (in this case the first 3 rows) 
delimeter = ";"


#azure specific settings
#Azure Files
conn_str = "DefaultEndpointsProtocol=https;AccountName=biomonistorage;AccountKey=xP9awCaC8m+/KmIduCH2xt5CD8iyjYZstqFPo0haOXrucxWTsMrGVwd7/WKVYaOHhCTqmIM5j/p6+CQtIXHAjg==;EndpointSuffix=core.windows.net"
share_name = "biomoni-storage"
azure_file_path = "Measurement-data/Experiment-data/data.csv"
push_to_azure = True
kwargs_push_azure_file = dict(connection_string = conn_str, share_name = share_name, azure_file_path = azure_file_path)


OPCUA_collector(url = url, Result_path = Result_path, data_name = data_name, cols_vs_id = cols_vs_id, root_ID = root_ID, delimeter = ";", sample_interval = 180, push_to_azure = True, initial_row_filler= initial_row_filler,  print_data_in_console= True,  kwargs_push_azure_file = kwargs_push_azure_file)





    