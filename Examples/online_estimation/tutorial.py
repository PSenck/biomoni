##https://docs.microsoft.com/de-de/azure/storage/files/storage-python-how-to-use-file-storage?tabs=python
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.fileshare import ShareServiceClient, ShareClient, ShareDirectoryClient, ShareFileClient


service_client = ShareServiceClient.from_connection_string(conn_str= conn_str)
share_name = "biomoni-storage"

print(service_client)


#This Function is to create a new empty file storage folder in your stargeaccount/file-share, damit wird die Freigabe erstellt wenn sie nicht vorhanden ist
# def create_file_share(connection_string, share_name):
#     try:
#         # Create a ShareClient from a connection string
#         share_client = ShareClient.from_connection_string(
#             connection_string, share_name, overwrite = overwrite)

#         print("Creating share:", share_name)
#         share_client.create_share(overwrite = True)

#     except ResourceExistsError as ex:
#         print("ResourceExistsError:", ex.message)
# create_file_share(conn_str, share_name)

# #Verzeichnis in Ordner Struktur anlegen
# def create_directory(connection_string, share_name, dir_name):
#     try:
#         # Create a ShareDirectoryClient from a connection string
#         dir_client = ShareDirectoryClient.from_connection_string(
#             connection_string, share_name, dir_name, overwrite = True)

#         print("Creating directory:", share_name + "/" + dir_name)
#         dir_client.create_directory()

#     except ResourceExistsError as ex:
#         print("ResourceExistsError:", ex.message)

# create_directory(connection_string= conn_str, share_name= share_name, dir_name = "bio-storage")

local_files = {"data" : "uploadfolder/data/hehe.txt", "metadata" : "uploadfolder/metadata_OPCUA.ods"}
destination_files = {"data" : "Measurement-data/Experiment-data/data.txt", "metadata" : "Measurement-data/metadata_OPCUA.ods"}

def upload_local_file(connection_string, local_file_path, share_name, dest_file_path):
    try:
        source_file = open(local_file_path, "rb")
        data = source_file.read()

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, dest_file_path)

        print("Uploading to:", share_name + "/" + dest_file_path)
        file_client.upload_file(data)

    except ResourceExistsError as ex:
        print("ResourceExistsError:", ex.message)

    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)

    except Exception as ex:
        print('Exception:')
        print(ex) 

[upload_local_file(conn_str, local_file_path= local, share_name= "biomoni-storage", dest_file_path= dest) for local, dest in zip(local_files.values(), destination_files.values())]

download_dir = {"data" : "Measurement-data/Experiment-data/", "metadata" : "Measurement-data/"}
download_file = {"data" : "data.txt", "metadata" : "metadata_OPCUA.ods"}
def download_azure_file(connection_string, share_name, dir_name, file_name):
    try:
        # Build the remote path
        source_file_path = dir_name + "/" + file_name

        # Add a prefix to the filename to 
        # distinguish it from the uploaded file
        dest_file_name = "DOWNLOADED-" + file_name

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, source_file_path)

        print("Downloading to:", dest_file_name)

        # Open a file for writing bytes on the local system
        with open(dest_file_name, "wb") as data:
            # Download the file from Azure into a stream
            stream = file_client.download_file()
            # Write the stream to the local file
            data.write(stream.readall())

    except ResourceNotFoundError as ex:
        print("ResourceNotFoundError:", ex.message)

[download_azure_file(conn_str, share_name= "biomoni-storage", dir_name= dir, file_name = f) for dir, f in zip(download_dir.values(), download_file.values())]