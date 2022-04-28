from biomoni.Experiment import Experiment
from biomoni import Yeast
import pandas as pd

## to better understand the code in the biomoni package you can just debug this script step for step, it involves nearly all important functions
################################################################################################################################################

#adapt ypur path
#Linux path
path = "/home/paul/pCloudDrive/Code/Messdaten" 

#windows path
#path = r"P:\Code\biomoni\Messdaten"
    
kwags_exp = dict(meta_path = "metadata.xlsx"
    , types = {"off" : "offline.csv", "on": "online.CSV", "CO2" : "CO2.dat"}
    , exp_dir_manual = None
    , index_ts = {"off" : 0, "on": 0, "CO2" : 0}

    , read_csv_settings = { "off" : dict(sep=";", encoding= 'unicode_escape', header = 0, usecols = None)
    , "on": dict(sep=";",encoding= "unicode_escape",decimal=",", skiprows=[1,2] , skipfooter=1, usecols = None, engine="python")
    , "CO2" : dict(sep=";", encoding= "unicode_escape", header = 0, skiprows=[0], usecols=[0,2,4], names =["ts","CO2", "p"])    }

    , to_datetime_settings = {"off" : dict(format = "%d.%m.%Y %H:%M", exact= False, errors = "coerce")
    , "on": dict(format = "%d.%m.%Y  %H:%M:%S", exact= False, errors = "coerce")
    , "CO2" : dict(format = "%d.%m.%Y %H:%M:%S", exact= False, errors = "coerce")   }

    , calc_rate = {"on" : "BASET"}
    , endpoint = "end1"
    , read_excel_settings = None)



experiment_dict = {exp : Experiment(path, exp, **kwags_exp) for exp in ["F4", "F5", "F6", "F7", "F8" ]}  #all experiments in a dictionary
experiment_dict["F8"].time_filter(dskey= "on", start = pd.to_datetime("14.12.2020  12:20:16")) #special time filter for experiment 8
[experiment_dict[exp].pop_dataframe("on") for exp in ["F4", "F5", "F6"]]   #delete online data in experiment 4,5,6 because of bad BASET_rate measurements 

y = Yeast()

y.estimate(experiment_dict)
y.report()