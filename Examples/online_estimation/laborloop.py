import os
import pathlib
import time
import pandas as pd
import csv
from datetime import datetime

from biomoni.Experiment import Experiment
from biomoni.Yeast import Yeast
from biomoni.visualize import visualize
from settings import Result_path, image_path, kwargs_experiment
from param_collection import p1


sub_paths = next(os.walk(Result_path))[1]       #yields the subsirectory in the given path
newest_results_dir = max([os.path.join(Result_path,i) for i in sub_paths], key=os.path.getmtime) #gives newest subdirectory
exp_dir_manual = newest_results_dir #Manually given experiment name (subfolder_name within path), can be used if the experiment identifier (exp_id which is also the index column in metadata) does not match with the folder name, e.g. when folder name is created automatically.

y = Yeast()

estimated_params = {"ts" : []}
for p in y.p.keys():
    estimated_params[p] = []
estimated_params = pd.DataFrame(estimated_params)

now = datetime.now().strftime("%d.%m.%Y_%H:%M")
param_filename = "estimated_params_" + now

param_file = os.path.join(newest_results_dir, param_filename) 
with open(param_file, 'w', newline = "") as f:       #csv file will be created #newline because open makes some extra lines, avoid by using newline = ""
    writer = csv.writer(f)
    writer.writerow(estimated_params.columns.values)       

figure_list = []


image_path = os.path.join(image_path, "images_" + now)
if not os.path.exists(image_path):
    os.mkdir(image_path)

while True:
    time.sleep(1)    # Sampling before each estimation

    Exp = Experiment(path = Result_path, exp_dir_manual = exp_dir_manual, **kwargs_experiment["online_est"])

    
    y.set_params(p1)    #change initial parameters to test estimation
    y.estimate(Exp, tau = 1, max_nfev = 100)     #max function evaluations #, max_nfev = 100  



    y.report()
    sim = y.simulate(Exp)
    #visualize(Exp, sim, column_dict = {"BASET_rate" : "cyan", "CO2" : "orange"}, secondary_y_cols = ["CO2"])
    figure_list.append(visualize(Exp,sim))

    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S") 

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
    fig.write_image(image_path + "/image" + now + ".png")




    



