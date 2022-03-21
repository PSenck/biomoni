import os
from file_manager import pull_azure_file, push_azure_file, create_directory

conn_str = "DefaultEndpointsProtocol=https;AccountName=biomonistorage;AccountKey=xP9awCaC8m+/KmIduCH2xt5CD8iyjYZstqFPo0haOXrucxWTsMrGVwd7/WKVYaOHhCTqmIM5j/p6+CQtIXHAjg==;EndpointSuffix=core.windows.net"
# share_name = "biomoni-storage"
# azure_file_path = "Measurement-data/Experiment-data/data.csv"
share_name = "crazystorage"
azure_file_path = "lelel/grellek/prellek/säbel/mäbel/mellek.txt"


#pull_azure_file(connection_string = conn_str, share_name = share_name, source_file_path = azure_file_path, local_path = None)

push_azure_file(data = "mellek.txt" ,connection_string= conn_str, share_name= share_name, azure_file_path= azure_file_path)