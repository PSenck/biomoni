##Settings for MFCS_mimic, Data_collector, Laborloop routine,
#This is the Settings script for the 1. MFCS_mimic, 2. Data_collector, 3. Laborloop routine, the first thing you have to do when you start is to adapt your paths (Exp_path and Result_path)
#Linux
Exp_path = "/home/paul/pCloudDrive/Code/biomoni/Messdaten" #path in which the experiment to be simulated is located. For the MFCS_mimic simualted data is returned, this data was simulated based on real data present in Exp_path
Result_path = "/home/paul/pCloudDrive/Code/biomoni/Messdaten/OPCUA" #path where Results (data from MFCS) are stored. The path where data recorded by the opcua client (data_collector) is stored and also the data used for online estimation in laborloop.

# #Windows 
# Exp_path = r"P:\Code\biomoni\Messdaten"    #path in which the experiment to be simulated is located. For the MFCS_mimic simualted data is returned, this data was simulated based on real data present in Exp_path
# Result_path = r"P:\Code\biomoni\Messdaten\OPCUA"    #path where Results (data from MFCS) are stored. The path where data recorded by the opcua client (data_collector) is stored and also the data used for online estimation in laborloop.



exp_id = "F7"   #The Experiment to simulate, within Exp_path
data_name = "data.csv"        #name of the csv file in which data will be saved
sample_interval = 60    #Time in sec in which a measured value is generated (server) or a measured value is read (client). 

#In the following are Settings to create an Experiment (kwargs_experiment) object and settings to estimate (kwargs_estimate), these are only used in the laborloop
kwargs_experiment = {       #setting to create Experiment object

"online_est" : dict (


    exp_id = "current_ferm",     #identifier to read correct data from the metadata
    meta_path = "metadata_OPCUA.ods",    #metadata location within path
    types = {"on_CO2" : data_name},
    index_ts = {"on_CO2" : 0},
    read_csv_settings = {"on_CO2" : dict(sep=";",encoding= "unicode_escape",decimal=",", skiprows=[1,2] , skipfooter=1, usecols = None, engine="python")},
    to_datetime_settings = {"on_CO2" : dict(format = "%d.%m.%Y  %H:%M:%S", exact= False, errors = "coerce") },
    calc_rate =dict(on_CO2 = "BASET"),
    read_excel_settings = dict(engine = "odf")

),

"offline_est" : dict(meta_path = "metadata.xlsx"
    , types = {"off" : "offline.csv", "on": "online.CSV", "CO2" : "CO2.dat"}
    , exp_dir_manual = None
    , index_ts = {"off" : 0, "on": 0, "CO2" : 0}

    , read_csv_settings = { "off" : dict(sep=";", header = 0, usecols = None)
    , "on": dict(sep=";",encoding= "unicode_escape",decimal=",", skiprows=[1,2] , skipfooter=1, usecols = None, engine="python")
    , "CO2" : dict(sep=";",header = 0, skiprows=[0], usecols=[0,2,4], names =["ts","CO2", "p"])    }

    , to_datetime_settings = {"off" : dict(format = "%d.%m.%Y %H:%M", exact= False, errors = "coerce")
    , "on": dict(format = "%d.%m.%Y  %H:%M:%S", exact= False, errors = "coerce")
    , "CO2" : dict(format = "%d.%m.%Y %H:%M:%S", exact= False, errors = "coerce")   }

    , calc_rate = {"on" : "BASET"}
    , endpoint = "end1"
    , read_excel_settings = None
    , smooth = {"on" : "BASET_rate"}
    , kwargs_smooth = dict(halflife=3, adjust= False)
)

}

kwargs_estimate = {         #settings to estimate

"online_est" : dict (
    tau = 1, 
    max_nfev = 30      #max function evaluations, maximum of iterations done in order to estimate
    )
}


#Settings required to build an OPC server, and an OPC client

url = "opc.tcp://127.0.0.1:4848"    #OPC server url and client

#Server settings for the MFCS_mimic module, create Variables and values that are getting returned from the Sartorius MFCS (fake) Unit 
#Units identity
units_id = dict(
FM_1 = ('ns=2;s="FM_1"', "FM_1"),       #e.g. Frau Menta 1 (process Unit)
FM_2 = ('ns=2;s="FM_2"', "FM_2"),
HM_3 = ('ns=2;s="HM_1"', "HM_1"),
HM_4 = ('ns=2;s="HM_4"', "HM_4")        #Herr Menta 4
)

#Variables_id
variables_id = dict(
BASET = ('ns=2;s="BASET_2"', "BASET_2"),
CO2 = ('ns=2;s="CO2"', "CO2"),
CO2_pressure = ('ns=2;s="CO2_p"', "CO2_pressure"),
ts = ('ns=2;s="PDatTime"', "PDatTime")
)

#Value_id
values_id = dict(
BASET = ('ns=2;s="Value_BASET_2"',"Value",0),        #default value is zero: gets changed anyway with the set method
CO2 = ('ns=2;s="Value_CO2"',"Value",0),
CO2_pressure = ('ns=2;s="CO2_pressure"',"Value",1.058),
ts = ('ns=2;s="Value_PDatTime"',"Value",0)
)


#Root identity: this is useful to get the values directly from the root node through root.get_child. This is used in the data collector.
#to get the value of the structure directly through all vraiebles created above (units, variables)
#Martins Anmerkung: überall statt 0: 2: um die Anpassung von python UA Server auf OPCUA-server von MFCS zu machen (außer bei Objects da bleibt 0)
#Meine Anmerkung: überall steht Value+Variable nur bei BASET_2, CO2, CO2_pressure und PDatTime steht nur Value....

nID_HM_4 = {
    'ACIDT': ["0:Objects","0:Units","0:HM_4","0:Variables","0:BALANCE_B1","0:Value_BALANCE_B1"],
    'BALANCE_A1': ["0:Objects","0:Units","0:HM_4","0:Variables","0:BALANCE_A1","0:Value_BALANCE_A1"],
    'BALANCE_B1':["0:Objects","0:Units","0:HM_4","0:Variables","0:BALANCE_B1","0:Value_BALANCE_B1"],
    'BASET_2':["0:Objects","0:Units","0:HM_4","0:Variables","0:BASET_2","0:Value"],
    'CO2':["0:Objects","0:Units","0:HM_4","0:Variables","0:CO2","0:Value"],     #No idea why Martin named it only Value here and not Value_Variable
    'CO2_pressure':["0:Objects","0:Units","0:HM_4","0:Variables","0:CO2_pressure","0:Value"],
    'ECO2_1':["0:Objects","0:Units","0:HM_4","0:Variables","0:ECO2_1","0:Value_ECO2_1"],
    'EO2_1':["0:Objects","0:Units","0:HM_4","0:Variables","0:EO2_1","0:Value_EO2_1"],
    'EXT_A1':["0:Objects","0:Units","0:HM_4","0:Variables","0:EXT_A1","0:Value_EXT_A1"],
    'EXT_B1':["0:Objects","0:Units","0:HM_4","0:Variables","0:EXT_B1","0:Value_EXT_B1"],
    'FOAMT_1':["0:Objects","0:Units","0:HM_4","0:Variables","0:FOAMT_1","0:Value_FOAMT_1"],
    'MFC_B1':["0:Objects","0:Units","0:HM_4","0:Variables","0:MFC_B1","0:Value_MFC_B1"],
    'MFC_C1':["0:Objects","0:Units","0:HM_4","0:Variables","0:MFC_C1","0:Value_MFC_C1"],
    'MFC_D1':["0:Objects","0:Units","0:HM_4","0:Variables","0:MFC_D1","0:Value_MFC_D1"],
    'O2SPT_1':["0:Objects","0:Units","0:HM_4","0:Variables","0:O2SPT_1","0:Value_O2SPT_1"],
    'PUMPT_A1':["0:Objects","0:Units","0:HM_4","0:Variables","0:PUMPT_A1","0:Value_PUMPT_A1"],
    'REDOX_1':["0:Objects","0:Units","0:HM_4","0:Variables","0:REDOX_1","0:Value_REDOX_1"],
    'SUBST_A1':["0:Objects","0:Units","0:HM_4","0:Variables","0:SUBST_A1","0:Value_SUBST_A1"],
    'SUBST_B1':["0:Objects","0:Units","0:HM_4","0:Variables","0:SUBST_B1","0:Value_SUBST_B1"],
    'SUBST_C1':["0:Objects","0:Units","0:HM_4","0:Variables","0:SUBST_C1","0:Value_SUBST_C1"],
    'TURB_1':["0:Objects","0:Units","0:HM_4","0:Variables","0:TURB_1","0:Value_TURB_1"],
    'VALVET_A1':["0:Objects","0:Units","0:HM_4","0:Variables","0:VALVET_A1","0:Value_VALVET_A1"],
    'VALVET_C1':["0:Objects","0:Units","0:HM_4","0:Variables","0:VALVET_C1","0:Value_VALVET_C1"],
    'VALVET_D1':["0:Objects","0:Units","0:HM_4","0:Variables","0:VALVET_D1","0:Value_VALVET_D1"],
    'VALVE_A1':["0:Objects","0:Units","0:HM_4","0:Variables","0:VALVE_A1","0:Value_VALVE_A1"],
    'VALVE_C1':["0:Objects","0:Units","0:HM_4","0:Variables","0:VALVE_C1","0:Value_VALVE_C1"],
    'VALVE_D1':["0:Objects","0:Units","0:HM_4","0:Variables","0:VALVE_D1","0:Value_VALVE_D1"],
    'PDatTime':["0:Objects","0:Units","0:HM_4","0:Variables","0:PDatTime","0:Value"],           
    'pHo_1':["0:Objects","0:Units","0:HM_4","0:Variables","0:pHo_1","0:Value_pHo_1"],
    'pO2o_1':["0:Objects","0:Units","0:HM_4","0:Variables","0:pO2o_1","0:Value_pO2o_1"],
}



#For the other Fermenters

#FM_1
nID_FM_1 = {
    'ACIDT': ["0:Objects","0:Units","0:FM_1","0:Variables","0:BALANCE_B1","0:Value_BALANCE_B1"],
    'BALANCE_A1': ["0:Objects","0:Units","0:FM_1","0:Variables","0:BALANCE_A1","0:Value_BALANCE_A1"],
    'BALANCE_B1':["0:Objects","0:Units","0:FM_1","0:Variables","0:BALANCE_B1","0:Value_BALANCE_B1"],
    'BASET_1':["0:Objects","0:Units","0:FM_1","0:Variables","0:BASET_1","0:Value_BASET_1"],
    'ECO2_1':["0:Objects","0:Units","0:FM_1","0:Variables","0:ECO2_1","0:Value_ECO2_1"],
    'EO2_1':["0:Objects","0:Units","0:FM_1","0:Variables","0:EO2_1","0:Value_EO2_1"],
    'EXT_A1':["0:Objects","0:Units","0:FM_1","0:Variables","0:EXT_A1","0:Value_EXT_A1"],
    'EXT_B1':["0:Objects","0:Units","0:FM_1","0:Variables","0:EXT_B1","0:Value_EXT_B1"],
    'FOAMT_1':["0:Objects","0:Units","0:FM_1","0:Variables","0:FOAMT_1","0:Value_FOAMT_1"],
    'MFC_B1':["0:Objects","0:Units","0:FM_1","0:Variables","0:MFC_B1","0:Value_MFC_B1"],
    'MFC_C1':["0:Objects","0:Units","0:FM_1","0:Variables","0:MFC_C1","0:Value_MFC_C1"],
    'MFC_D1':["0:Objects","0:Units","0:FM_1","0:Variables","0:MFC_D1","0:Value_MFC_D1"],
    'O2SPT_1':["0:Objects","0:Units","0:FM_1","0:Variables","0:O2SPT_1","0:Value_O2SPT_1"],
    'PUMPT_A1':["0:Objects","0:Units","0:FM_1","0:Variables","0:PUMPT_A1","0:Value_PUMPT_A1"],
    'REDOX_1':["0:Objects","0:Units","0:FM_1","0:Variables","0:REDOX_1","0:Value_REDOX_1"],
    'SUBST_A1':["0:Objects","0:Units","0:FM_1","0:Variables","0:SUBST_A1","0:Value_SUBST_A1"],
    'SUBST_B1':["0:Objects","0:Units","0:FM_1","0:Variables","0:SUBST_B1","0:Value_SUBST_B1"],
    'SUBST_C1':["0:Objects","0:Units","0:FM_1","0:Variables","0:SUBST_C1","0:Value_SUBST_C1"],
    'TURB_1':["0:Objects","0:Units","0:FM_1","0:Variables","0:TURB_1","0:Value_TURB_1"],
    'VALVET_A1':["0:Objects","0:Units","0:FM_1","0:Variables","0:VALVET_A1","0:Value_VALVET_A1"],
    'VALVET_C1':["0:Objects","0:Units","0:FM_1","0:Variables","0:VALVET_C1","0:Value_VALVET_C1"],
    'VALVET_D1':["0:Objects","0:Units","0:FM_1","0:Variables","0:VALVET_D1","0:Value_VALVET_D1"],
    'VALVE_A1':["0:Objects","0:Units","0:FM_1","0:Variables","0:VALVE_A1","0:Value_VALVE_A1"],
    'VALVE_C1':["0:Objects","0:Units","0:FM_1","0:Variables","0:VALVE_C1","0:Value_VALVE_C1"],
    'VALVE_D1':["0:Objects","0:Units","0:FM_1","0:Variables","0:VALVE_D1","0:Value_VALVE_D1"],
    'pHo_1':["0:Objects","0:Units","0:FM_1","0:Variables","0:pHo_1","0:Value_pHo_1"],
    'pO2o_1':["0:Objects","0:Units","0:FM_1","0:Variables","0:pO2o_1","0:Value_pO2o_1"],
}

#FM_2
nID_FM_2 = {
    'ACIDT': ["0:Objects","0:Units","0:FM_2","0:Variables","0:BALANCE_B1","0:Value_BALANCE_B1"],
    'BALANCE_A1': ["0:Objects","0:Units","0:FM_2","0:Variables","0:BALANCE_A1","0:Value_BALANCE_A1"],
    'BALANCE_B1':["0:Objects","0:Units","0:FM_2","0:Variables","0:BALANCE_B1","0:Value_BALANCE_B1"],
    'BASET_1':["0:Objects","0:Units","0:FM_2","0:Variables","0:BASET_1","0:Value_BASET_1"],
    'ECO2_1':["0:Objects","0:Units","0:FM_2","0:Variables","0:ECO2_1","0:Value_ECO2_1"],
    'EO2_1':["0:Objects","0:Units","0:FM_2","0:Variables","0:EO2_1","0:Value_EO2_1"],
    'EXT_A1':["0:Objects","0:Units","0:FM_2","0:Variables","0:EXT_A1","0:Value_EXT_A1"],
    'EXT_B1':["0:Objects","0:Units","0:FM_2","0:Variables","0:EXT_B1","0:Value_EXT_B1"],
    'FOAMT_1':["0:Objects","0:Units","0:FM_2","0:Variables","0:FOAMT_1","0:Value_FOAMT_1"],
    'MFC_B1':["0:Objects","0:Units","0:FM_2","0:Variables","0:MFC_B1","0:Value_MFC_B1"],
    'MFC_C1':["0:Objects","0:Units","0:FM_2","0:Variables","0:MFC_C1","0:Value_MFC_C1"],
    'MFC_D1':["0:Objects","0:Units","0:FM_2","0:Variables","0:MFC_D1","0:Value_MFC_D1"],
    'O2SPT_1':["0:Objects","0:Units","0:FM_2","0:Variables","0:O2SPT_1","0:Value_O2SPT_1"],
    'PUMPT_A1':["0:Objects","0:Units","0:FM_2","0:Variables","0:PUMPT_A1","0:Value_PUMPT_A1"],
    'REDOX_1':["0:Objects","0:Units","0:FM_2","0:Variables","0:REDOX_1","0:Value_REDOX_1"],
    'SUBST_A1':["0:Objects","0:Units","0:FM_2","0:Variables","0:SUBST_A1","0:Value_SUBST_A1"],
    'SUBST_B1':["0:Objects","0:Units","0:FM_2","0:Variables","0:SUBST_B1","0:Value_SUBST_B1"],
    'SUBST_C1':["0:Objects","0:Units","0:FM_2","0:Variables","0:SUBST_C1","0:Value_SUBST_C1"],
    'TURB_1':["0:Objects","0:Units","0:FM_2","0:Variables","0:TURB_1","0:Value_TURB_1"],
    'VALVET_A1':["0:Objects","0:Units","0:FM_2","0:Variables","0:VALVET_A1","0:Value_VALVET_A1"],
    'VALVET_C1':["0:Objects","0:Units","0:FM_2","0:Variables","0:VALVET_C1","0:Value_VALVET_C1"],
    'VALVET_D1':["0:Objects","0:Units","0:FM_2","0:Variables","0:VALVET_D1","0:Value_VALVET_D1"],
    'VALVE_A1':["0:Objects","0:Units","0:FM_2","0:Variables","0:VALVE_A1","0:Value_VALVE_A1"],
    'VALVE_C1':["0:Objects","0:Units","0:FM_2","0:Variables","0:VALVE_C1","0:Value_VALVE_C1"],
    'VALVE_D1':["0:Objects","0:Units","0:FM_2","0:Variables","0:VALVE_D1","0:Value_VALVE_D1"],
    'pHo_1':["0:Objects","0:Units","0:FM_2","0:Variables","0:pHo_1","0:Value_pHo_1"],
    'pO2o_1':["0:Objects","0:Units","0:FM_2","0:Variables","0:pO2o_1","0:Value_pO2o_1"],
}

#HM_3
nID_HM_3 = {
    'ACIDT': ["0:Objects","0:Units","0:HM_3","0:Variables","0:BALANCE_B1","0:Value_BALANCE_B1"],
    'BALANCE_A1': ["0:Objects","0:Units","0:HM_3","0:Variables","0:BALANCE_A1","0:Value_BALANCE_A1"],
    'BALANCE_B1':["0:Objects","0:Units","0:HM_3","0:Variables","0:BALANCE_B1","0:Value_BALANCE_B1"],
    'BASET_1':["0:Objects","0:Units","0:HM_3","0:Variables","0:BASET_1","0:Value_BASET_1"],
    'ECO2_1':["0:Objects","0:Units","0:HM_3","0:Variables","0:ECO2_1","0:Value_ECO2_1"],
    'EO2_1':["0:Objects","0:Units","0:HM_3","0:Variables","0:EO2_1","0:Value_EO2_1"],
    'EXT_A1':["0:Objects","0:Units","0:HM_3","0:Variables","0:EXT_A1","0:Value_EXT_A1"],
    'EXT_B1':["0:Objects","0:Units","0:HM_3","0:Variables","0:EXT_B1","0:Value_EXT_B1"],
    'FOAMT_1':["0:Objects","0:Units","0:HM_3","0:Variables","0:FOAMT_1","0:Value_FOAMT_1"],
    'MFC_B1':["0:Objects","0:Units","0:HM_3","0:Variables","0:MFC_B1","0:Value_MFC_B1"],
    'MFC_C1':["0:Objects","0:Units","0:HM_3","0:Variables","0:MFC_C1","0:Value_MFC_C1"],
    'MFC_D1':["0:Objects","0:Units","0:HM_3","0:Variables","0:MFC_D1","0:Value_MFC_D1"],
    'O2SPT_1':["0:Objects","0:Units","0:HM_3","0:Variables","0:O2SPT_1","0:Value_O2SPT_1"],
    'PUMPT_A1':["0:Objects","0:Units","0:HM_3","0:Variables","0:PUMPT_A1","0:Value_PUMPT_A1"],
    'REDOX_1':["0:Objects","0:Units","0:HM_3","0:Variables","0:REDOX_1","0:Value_REDOX_1"],
    'SUBST_A1':["0:Objects","0:Units","0:HM_3","0:Variables","0:SUBST_A1","0:Value_SUBST_A1"],
    'SUBST_B1':["0:Objects","0:Units","0:HM_3","0:Variables","0:SUBST_B1","0:Value_SUBST_B1"],
    'SUBST_C1':["0:Objects","0:Units","0:HM_3","0:Variables","0:SUBST_C1","0:Value_SUBST_C1"],
    'TURB_1':["0:Objects","0:Units","0:HM_3","0:Variables","0:TURB_1","0:Value_TURB_1"],
    'VALVET_A1':["0:Objects","0:Units","0:HM_3","0:Variables","0:VALVET_A1","0:Value_VALVET_A1"],
    'VALVET_C1':["0:Objects","0:Units","0:HM_3","0:Variables","0:VALVET_C1","0:Value_VALVET_C1"],
    'VALVET_D1':["0:Objects","0:Units","0:HM_3","0:Variables","0:VALVET_D1","0:Value_VALVET_D1"],
    'VALVE_A1':["0:Objects","0:Units","0:HM_3","0:Variables","0:VALVE_A1","0:Value_VALVE_A1"],
    'VALVE_C1':["0:Objects","0:Units","0:HM_3","0:Variables","0:VALVE_C1","0:Value_VALVE_C1"],
    'VALVE_D1':["0:Objects","0:Units","0:HM_3","0:Variables","0:VALVE_D1","0:Value_VALVE_D1"],
    'pHo_1':["0:Objects","0:Units","0:HM_3","0:Variables","0:pHo_1","0:Value_pHo_1"],
    'pO2o_1':["0:Objects","0:Units","0:HM_3","0:Variables","0:pO2o_1","0:Value_pO2o_1"],
}