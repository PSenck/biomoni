##https://docs.microsoft.com/de-de/azure/storage/files/storage-python-how-to-use-file-storage?tabs=python
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError, HttpResponseError

from azure.storage.fileshare import ShareServiceClient, ShareClient, ShareDirectoryClient, ShareFileClient

from opcua import Client
import time
import pandas as pd
import os
import csv
import errno
from datetime import datetime
import sys


def OPCUA_collector(url, Result_path, data_name, cols_vs_id, root_ID, delimeter = ","
    , initial_row_filler = None, sample_interval = 60, create_ts = False, ts_format = "%d.%m.%Y  %H:%M:%S", print_data_in_console = False
    , push_to_azure = False, kwargs_push_azure_file = None):
    """Function to collect values from OPCUA Server over the root ID and write them into a csv file.

    Args:
        url (str): url to connect to OPCUA Server.
        Result_path (str): place where to store the csv file.
        data_name: name of the csv file itself.
        cols_vs_id (dict): dictionary with key: colum name in csv file and value: id of respective value in root_ID.
        root_ID (dict): root ID for different values returned by the OPCUA server.



    Kwargs:
        delimeter (str): separator to split columns.
        initial_row_filler (list of lists): will fill the first rows of the csv file (after the column names).
        sample_interval (int): sample interval in seconds.
        create_ts (bool): Create timestamp everytime OPCUA_collector is sampling (within evry loop iteration). Nevertheless it would be more acurate to use the timestamps given from the OPCUA Server directly (like PDatTime) instead of create on here.
        ts_format (str): Disired Time Format if create_ts is True.
        print_data_in_console (bool): show the sampled data as appending pd.DataFrame in the console (only for control pruposes).
        push_to_azure (bool): push the csv file directly to azure.
        kwargs_push_azure_file (dict): Keyword arguments for the function push_azure_file.
 
    """
    

    
    cols = list(cols_vs_id.keys())

    if create_ts == True:
        cols.insert(0, "ts")

    data = {col : [] for col in cols}
    data = pd.DataFrame(data)

    if initial_row_filler is not None:
        initial_row_filler = [row * len(cols) for row in initial_row_filler]
        initial_content = [cols, *initial_row_filler]
    else:
        initial_content = [cols]


    csv_name = os.path.join(Result_path, data_name) 
    with open(csv_name, 'w', newline = "") as f:       #csv file will be created #newline because open makes some extra lines, avoid by using newline = ""
        writer = csv.writer(f, delimiter = delimeter)
        [writer.writerow(i) for i in (initial_content)]       #[] for 1 empty row

    client = Client(url)
    client.connect()
    print("client connected")
    root = client.get_root_node()   #root_node
        
    while True:
        
        Values_dict = {}
        if create_ts == True:
            Values_dict["ts"] = datetime.now().strftime(ts_format) 

        for name, id in cols_vs_id.items():
            Values_dict[name] = root.get_child(root_ID[id]).get_value()

        appendix = pd.Series(Values_dict)

        assert list(appendix.index) == cols, "The cols in the CSV file and the cols in the appendix much match in the same row"

        #append csv file row by row
        with open(csv_name, 'a', newline = "") as f:
            writer = csv.writer(f, delimiter = ";")
            writer.writerow(appendix)

        #just to show the data as pd.DataFrame
        data = data.append(appendix, ignore_index=True) #append data row by row

        if print_data_in_console is True:
            print(data)


        if push_to_azure is True:
        
            push_azure_file(data = csv_name, **kwargs_push_azure_file)  #this overwrites the csv file on azure evrytime, maybe there is also a for appending it directly. I think with blobs it is possible but no solution found for azure files yet.

        time.sleep(sample_interval)




def create_file_share(connection_string, share_name):
    """""Function to create file share, you can also create it in the browser.

    Args:
        connection_string (str): connection string of your storage account in azure (Key 1)
        share_name (str): name of the file share you want to create

    
    """
    try:
        # Create a ShareClient from a connection string
        share_client = ShareClient.from_connection_string(
            connection_string, share_name)

        print("Creating share:", share_name)
        share_client.create_share()

    except ResourceExistsError as ex:
        print("ResourceExistsError:", ex.message)


# #Verzeichnis in Ordner Struktur anlegen
def create_directory(connection_string, share_name, dir_name, ignore_ResourceExistsError = False):
    """Function to create a directory, you can also create it in the browser.
    
    Args:
        connection_string (str): connection string of your storage account in azure (Key 1)
        share_name (str): name of existing file share where you want to create the directory
        dir_name: name of the directory you want to create

    Kwargs:
        ignore_ResourceExistsError (str): If directory already exists, it will raise a message (False) or not (True)

    """
    try:
        # Create a ShareDirectoryClient from a connection string
        dir_client = ShareDirectoryClient.from_connection_string(
            connection_string, share_name, dir_name)

        dir_client.create_directory()
        print("Creating directory:", os.path.join(share_name, dir_name))

    except ResourceExistsError as ex:
        if ignore_ResourceExistsError is True:
            return
        elif ignore_ResourceExistsError is False:
            print("ResourceExistsError:", ex.message)
        else:
            raise TypeError("ignore_ResourceExistsError must be True or False")
        




def push_azure_file(data, connection_string, share_name, azure_file_path):
    """Function to upload files in directories on azure, if the file share does not exist you will be asked if you want to create one, if the directory does not exist within the file share, you will be asked if you want to create one.

    Args:
        data (file): data you want to upload. e.g. 'hello.txt'.
        connection_string (str): connection string of your storage account in azure (Key 1)
        share_name (str): name of the file share 
        azure_file_path (str): path name of the file on azure e.g. 'storage/data/hello.txt'.

    """


    share_client = ShareClient.from_connection_string(connection_string, share_name)
    azure_dir = os.path.dirname(azure_file_path)

    try:
        share_client.get_share_stats()      #if there is no share client there can be no stats, maybe there are some better methods like share_client.exists() or sth

    except HttpResponseError as ex:
        decision = ""

        while decision != "y" and decision != "n":

            decision = input("There is no Azure file share named '{0}', would you like to create one? [y/n] : ".format(share_name))
            if decision == "y":
                create_file_share(connection_string, share_name)
            elif decision == "n":
                print("The dowload was stopped")
            else:
                print("Invalid input")
    try: 
        list(share_client.list_directories_and_files(azure_dir))
        
    except:
        decision = ""
        while decision != "y" and decision != "n":
            decision = input("There is no path named '{0}' in the Azure file share '{1}', would you like to create one? [y/n] : ".format(azure_dir, share_name))
            if decision == "y":

                path = os.path.normpath(azure_dir)
                path_list = path.split(os.sep)

                l = []
                i = 0
                for p in path_list:     #this is done because in azure you can not create paths recursively, you can not create nested directory directly, the parent path must exist, so you have to create them one by one ...
                    l.append(p)
                    if i > 0:
                        path = os.path.join(*l)
                    else:
                        path = p
                    i += 1
                    create_directory(connection_string, share_name, dir_name = path, ignore_ResourceExistsError = True)
                    
    
                
            elif decision == "n":
                print("The dowload was stopped")
            else:
                print("Invalid input")
        

    try:
        source_file = open(data, "rb")
        data = source_file.read()

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, azure_file_path)

        print("Uploading to:", share_name + "/" + azure_file_path)
        file_client.upload_file(data)

    except ResourceExistsError as ex:
        print("ResourceExistsError:", ex.message)

    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)

    # except Exception as ex:
    #     print('Exception:')
    #     print(ex) 


import time

def pull_azure_file(connection_string, share_name, azure_file_path, local_path = None):
    """Function to download files from azure and save them in a local directory.

    Args:
        connection_string (str): connection string of your storage account in azure (Key 1)
        share_name (str): name of the file share 
        azure_file_path (str): path name of the file on azure e.g. 'storage/data/hello.txt'.
        local_path (str): name of the local file path e.g. /downloads/hello_downloaded.txt. If local_path is not given (=None), the local path will get the name of azure_file_path. if the directory does not exist one will be created. 

    """

    share_client = ShareClient.from_connection_string(connection_string, share_name)


    try:
        share_client.get_share_properties()
        
    except Exception as ex:
        raise ex
        

    if local_path is None:
        local_path = azure_file_path
    
    try:            #Path will be created if it does not already exists
        os.makedirs(os.path.dirname(local_path))
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass


    try:

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, azure_file_path)

        print("Downloading to:", local_path)

        # Open a file for writing bytes on the local system
        with open(local_path, "wb") as data:
            # Download the file from Azure into a stream
            stream = file_client.download_file()
            # Write the stream to the local file
            data.write(stream.readall())

    except ResourceExistsError as ex:
        raise ex
        #print("ResourceExistsError:", ex.message)

    except ResourceNotFoundError as ex:
        raise ex
        #sys.exit("The file {0} was not found in the directory {1} on azure, downlaod was stopped".format(os.path.basename(azure_file_path) , os.path.dirname(azure_file_path))) 


    # except Exception as ex:
    #     print('Exception:')
    #     print(ex) 








# from azure.storage.blob.baseblobservice.BaseBlobService import AppendBlobService
# def append_data_to_blob(data, connection_string , account_name, container_name, blob_name):
#     """Function to append blobs (outdated)
#     """
#     service = AppendBlobService(account_name= account_name, account_key=connection_string)
#     try:
#         service.append_blob_from_text(container_name=container_name, blob_name=blob_name, text = data)  #try to write in blob
#     except:
#         service.create_blob(container_name=container_name, blob_name=blob_name) #make new blob if it does no exist
#         service.append_blob_from_text(container_name=container_name, blob_name=blob_name, text = data) 
#     print('Data Appended to Blob Successfully.')