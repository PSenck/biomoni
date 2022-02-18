#Settings required to run the dash app


Variables = {
    "typ1" : dict(measurement_vars = ["CO2", "BASET_rate"],  simulated_vars = ["cX", "cS", "cE", "CO2", "BASET_rate"]),

    "typ2" : dict(measurement_vars = ["cX", "cS", "cE", "CO2", "BASET_rate"],  simulated_vars = ["cX", "cS", "cE", "CO2", "BASET_rate"])

}






kwargs_experiment = {       #setting to create Experiment object

    "typ1" : dict (


    exp_id = "current_ferm",     #identifier to read correct data from the metadata
    meta_path = "metadata_OPCUA.ods",    #metadata location within path
    types = {"on_CO2" : "data_1"},
    index_ts = {"on_CO2" : 0},
    read_csv_settings = {"on_CO2" : dict(sep=";",encoding= "unicode_escape",decimal=",", skiprows=[1,2] , skipfooter=1, usecols = None, engine="python")},
    to_datetime_settings = {"on_CO2" : dict(format = "%d.%m.%Y  %H:%M:%S", exact= False, errors = "coerce") },
    calc_rate =("on_CO2", "BASET"),
    read_excel_settings = dict(engine = "odf")

    ),

    "typ2": dict(

    exp_id = "F7", meta_path = "metadata.xlsx"
    , types = {"off" : "offline.csv", "on": "online.CSV", "CO2" : "CO2.dat"}
    , index_ts = {"off" : 0, "on": 0, "CO2" : 0}

    , read_csv_settings = { "off" : dict(sep=";", encoding= 'unicode_escape', header = 0, usecols = None)
    , "on": dict(sep=";",encoding= "unicode_escape",decimal=",", skiprows=[1,2] , skipfooter=1, usecols = None, engine="python")
    , "CO2" : dict(sep=";", encoding= "unicode_escape", header = 0, skiprows=[0], usecols=[0,2,4], names =["ts","CO2", "p"])    }

    , to_datetime_settings = {"off" : dict(format = "%d.%m.%Y %H:%M", exact= False, errors = "coerce")
    , "on": dict(format = "%d.%m.%Y  %H:%M:%S", exact= False, errors = "coerce")
    , "CO2" : dict(format = "%d.%m.%Y %H:%M:%S", exact= False, errors = "coerce")   }

    , calc_rate = ("on", "BASET")
    , exp_dir_manual = None
    , endpoint = "end1"
    , read_excel_settings = None

    )

}

kwargs_estimate = {         #settings to estimate

    "typ1" : dict (
    tau = 1, 
    max_nfev = 100      #max function evaluations
    ),

    "typ2" : dict()

}
