import os
import pathlib
import time
import pandas as pd
import csv
from datetime import datetime
import errno
from biomoni.Experiment import Experiment
from biomoni.Yeast import Yeast
from biomoni.Model import CustomEstimationError
from biomoni.visualize import visualize
from settings import Result_path, kwargs_experiment, data_name
from param_collection import p1
from file_manager import pull_azure_file

# #1: Getting files from the automatically generated local file store, either comment out 1 or 2

sub_paths = next(os.walk(Result_path))[1]       #yields the subsirectory in the given path
newest_results_dir = max([os.path.join(Result_path,i) for i in sub_paths], key=os.path.getmtime) #gives newest subdirectory
path = Result_path
exp_dir_manual = newest_results_dir #Manually given experiment name (subfolder_name within path), can be used if the experiment identifier (exp_id which is also the index column in metadata) does not match with the folder name, e.g. when folder name is created automatically.


##2: Pulling files from Azure file share store, either comment out 1 or 2
##specify paths on azure where the data is stored

# conn_str = "DefaultEndpointsProtocol=https;AccountName=biomonistorage;AccountKey=hwA0oCscA7HbTxYvkyainLR/5WrVk3lBkfsiCTJEbQCTAur5BHddOVnRxJlgt0iSxqxufqBmQUZvGCk3epXXBQ==;EndpointSuffix=core.windows.net"
# share_name = "biomoni-storage"  #file share name
# azure_exp_file_path = "Measurement-data/current_ferm/data.csv"   #file path on azure for experiment data
# azure_metadata_file_path = "Measurement-data/metadata_OPCUA.ods"

# local_exp_file_path = azure_exp_file_path
# local_metadata_file_path = azure_metadata_file_path
# [pull_azure_file(connection_string= conn_str, share_name= share_name, azure_file_path= cloud, local_path= local)  for cloud, local in zip([azure_exp_file_path, azure_metadata_file_path], [local_exp_file_path, local_metadata_file_path]) ]
# path = os.path.dirname(local_metadata_file_path)
# exp_dir_manual = os.path.dirname(local_exp_file_path)



#The Laborloop routine starts here
y = Yeast()

estimated_params = {"ts" : []}
for p in y.p.keys():
    estimated_params[p] = []
estimated_params = pd.DataFrame(estimated_params)

param_dir = os.path.join(exp_dir_manual, "estimated_params")
image_dir = os.path.join(exp_dir_manual, "images")


now = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
param_filename = "estimated_params_" + now
image_dir = os.path.join(image_dir, "images_" + now)

for p in [param_dir, image_dir]:
    try:            #Path will be created if it does not already exists
        os.makedirs(p)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

param_file = os.path.join(param_dir, param_filename) 
with open(param_file, 'w', newline = "") as f:       #csv file will be created #newline because open makes some extra lines, avoid by using newline = ""
    writer = csv.writer(f)
    writer.writerow(estimated_params.columns.values)       

figure_list = []

try:
    Exp = Experiment(path = path, exp_dir_manual = exp_dir_manual, **kwargs_experiment["online_est"])
except TypeError as TE:

    print(TE.message)


###Nur zum Abfangen für das Problem mit zu wneig Datenpunkten####
##############################################################
# i = 0
# while i == 0:
#     try:
#         Exp = Experiment(path = path, exp_dir_manual = exp_dir_manual, **kwargs_experiment["online_est"])
#         y.set_params(p1)    #change initial parameters to test estimation
#         y.estimate(Exp, tau = 1, max_nfev = 2)     #max function evaluations #, max_nfev = 100
#         i = 1
#         print("The Estimation loop begins")
        
#     except CustomEstimationError:
#         print("Not enough data points sampled")
#         time.sleep(10)
#     except IndexError:
#         print("Not enough data points sampled")
#         time.sleep(10)

    

# y = Yeast()
# y.set_params(p1)

# variables = y.variables
# p = y.p

# param_vary_true_list = []       #generate a list with all parameters that are set as fit parameters (vary = True), this is done to compare the length of it with the numbe rof measurement points. If the number of measurement points is less than the number of fit parameters, the optimization wont work and should raise an Error (CustomEstimationError).
# for i in list(p):
#     if p[i].vary == True:
#         param_vary_true_list.append(i)
# param_vary_true_list = param_vary_true_list

# i = 0
# while i == 0:
#     Exp = Experiment(path = path, exp_dir_manual = exp_dir_manual, **kwargs_experiment["online_est"])
#     length_data_points = 0
#     for df in Exp.dataset.values():
#         for col in df:
#             if col in variables:
#                 cols_no_nan = df[col].dropna()
#                 length_data_points += len(cols_no_nan)
    
#     if length_data_points < len(param_vary_true_list):
#         print("Not enough data points sampled")
#         time.sleep(10)
#     else: 
#         print("The Estimation loop begins")
#         i = 1
    

################################################################

while True:
    time.sleep(1)    # Sampling before each estimation

    Exp = Experiment(path = path, exp_dir_manual = exp_dir_manual, **kwargs_experiment["online_est"])

    
    y.set_params(p1)    #change initial parameters to test estimation
    y.estimate(Exp, tau = 1, max_nfev = 100)     #max function evaluations #, max_nfev = 100  



    y.report()
    sim = y.simulate(Exp)
    #visualize(Exp, sim, column_dict = {"BASET_rate" : "cyan", "CO2" : "orange"}, secondary_y_cols = ["CO2"])
    figure_list.append(visualize(Exp,sim))

    now = datetime.now().strftime("%d.%m.%Y %H-%M-%S") 

    appendix = {"ts" : now }
    for p, value in y.p.items():
        appendix[p] = value.value
    
    appendix = pd.Series(appendix)

    #append csv file row by row
    with open(param_file, 'a', newline = "") as f:
        writer = csv.writer(f)
        writer.writerow(appendix)
    
    fig = visualize(Exp,sim, title = now)
    fig.show()
    figure_list.append(fig)
    fig.write_image(image_dir + "/image" + now + ".png")



#Improper input: func input vector length N=4 must not exceed func output vector length M=3
    



