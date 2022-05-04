# How to use the biomoni package in terms of online an estimation?
In this example, data from a Sartorius MFCS unit are automatically simulated and released via an OPC-UA server.

The following description demonstrates the online estimation using an artificial OPC-UA Server `MFCS_mimic.py`. If you do a real online estimation with data from the lab, the only thing which is different from this description is that there is no artificial OPC-UA Server like `MFCS_mimic.py`. In that case, this module is substituted with the OPC-UA Server of the measurement device. When estimating based on lab data, just replace `MFCS_mimic.py` with the OPC-UA Server of the measurement device. You may have to adapt the URL in `settings` to the URL given by the device.

The script `MFCS_mimic.py` first simulates data based on an existing Experiment in the `Exp_path` directory. The simulated data is then sent via an OPC UA server. The script `Data_collector` connects then to the OPC UA Server via the function `OPCUA_collector` in `biomoni.file_manager`. The picture `MFCS_scheme.png` shows the structure of the OPC-UA Server that is getting build up in `MFCS_mimic.py`. The values are  accessed  via the `root_ID` (e.g. `nID_HM_4` for device herr Menta 4). When using the `MFCS_mimic.py` script as OPC-UA Server it is mimicked from the MFCS Unit in G015 HS-Mannheim, the strings in root_ID's (like `nID_HM_4 `) in the `settings` should be written with zeros, likes this:
`'BASET_2':["0:Objects","0:Units","0:HM_4","0:Variables","0:BASET_2","0:Value"` but if you are in G015 at the HS Mannheim and the Sartorius device is the OPC-UA Server. You may have to change the zeros with a 2 (except for "Objects"), it should kook like this then:
`'BASET_2':["0:Objects","2:Units","2:HM_4","2:Variables","2:BASET_2","2:Value"`. The script `Data_collector` saves the data accessed via OPC-UA then in the directory `Result_path`, There is a new folder named after the current datetime with a data file named  `data_name` (name is set in `settings`). This file will be appended as long `Data_collector` is running. If the argument `push_to_azure` in the function `OPCUA_collector` used in `Data_collector` is set to `True` and if you have a Azure account with a storage account and a file share  and if you have given the correct `Connection_string` then the files will also be uploaded from `Data_collector` to Azure.
The script `laborloop.py` is the actual online estimation routine. It estimates based on the file that is getting appended on azure or on your local device in `Result_path`. To use the data from the local device comment in `1` and if you want to use the data on azure comment in `2` in `laborloop.py`.  Estimated parameters and images of the current timestamps are saved in `Result_path`. 

Run with current settings:
To run the code with all the settings already saved just adapt the `Exp_path` and the `Result_path` in `settings`. Then start `MFCS_mimic.py`, `Data_collector` and then `laborloop.py`.

To change settings and do your own online estimations:
To do an online Estimation with data getting released via OPC-UA, the following steps must be done:
1. `open param_collection` and enter for `p0` the parameter vector for which the simulated data should be generated. `p1` is the start parameter vector that is used in the online estimation in `laborloop`. `p1` should differ from `p0` before the estimation. After the estimation ideally the parameters `p0` should be found again.
2. open `settings` and adjust the following:
    • `url` = OPC-UA Server url
    • `Simulation_path` = path where the Experiments are. based on the Experiments there will be a simulation to create synthetical data to be send by the OPC UA Server.
    • `exp_id` = identifier of one idividual Experiment to be simulated
    • `Result_path` = path where the results will be stored.
    • `data_name` = name of the csv file into which the data will be written.
    • `sample_interval` = in seconds
    • All the Node ids
3. Execute the module `MFCS_mimic` to simulate MFCS data as OPC-UA Server
4. Execute the module `Data_collector` which is an OPC-UA client and pulls data from the OPC-UA server and stores it as a csv file in the Results_path.
5. Start the module `labloop`, be sure that the metadata for the simulation contains the same values as the metadata for the estimation.
