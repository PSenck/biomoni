from copy import deepcopy
from biomoni import Experiment, Yeast
from biomoni import visualize
import os 
import pathlib
from datetime import datetime
import numpy as np
import pandas as pd

import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Format
from dash.dependencies import Input, Output, State
from settings_dash import kwargs_experiment, kwargs_estimate, measurement_vars, simulated_vars, fitparams

from dash.long_callback import DiskcacheLongCallbackManager
import diskcache


from plotly.subplots import make_subplots
import plotly.graph_objs as go
import json



#Getting the main path 
Result_path = r"P:\Code\biomoni\Messdaten\OPCUA"        #pfad kann in settings.py
Result_path = "/home/paul/Desktop/pCloudDrive/Code/biomoni/Messdaten/OPCUA" 

path = Result_path

sub_paths = next(os.walk(Result_path))[1]       #yields the subsirectory in the given path
newest_results_dir = max([os.path.join(Result_path,i) for i in sub_paths], key=os.path.getmtime) #gives newest subdirectory
exp_dir_manual = newest_results_dir     #manually given subdirectory with measurement data because exp_id does not match with the actual directory in this case
kwargs_experiment["online_est"]["exp_dir_manual"] = exp_dir_manual      #add the directory to the key word arguments

#This code block are asignments, in order to work with your individual data, use your Experiment class and the respective options to run their constructors
Exp_class = Experiment      #assign your Experiment class to Exp_class
model_class = Yeast         #assign your Model class to model_class
experiment_options = kwargs_experiment["online_est"]       #use ur options to create an Experiment
estimation_options = kwargs_estimate["online_est"]         #use ur options to estimate

#create Experiment object and Model object with respective settings
Exp_init = Exp_class(path, **experiment_options)
y_init = model_class()
y_init.estimate(Exp_init, **estimation_options) 

all_vars = set([*measurement_vars, *simulated_vars])    #All variables only once, used to display the options in the dropdown at the initial callback



#color dict to style your layout
colors = {
    "background": "oxy",
    "text": "green",
    "settings" : "lightyellow",
    "table_header" : "red",
    "table_background" : "grey"
}

#external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]   #external stylesheets to style your layout
#cache = diskcache.Cache("./cache") #options for long_callback with cache
#long_callback_manager = DiskcacheLongCallbackManager(cache)    #options for long_callback with cache

#Create dash app
app = dash.Dash(__name__)     #external_stylesheets = external_stylesheets      #, long_callback_manager = long_callback_manager


def generate_table(dataframe, no_cols = []):         
    "Function to create a HTML table from pandas dataframe"
    columns = [col for col in dataframe.columns if col not in no_cols]
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in columns
            ]) for i in range(len(dataframe))       #, style = {"color" : colors["text"]}
        ])
    ])


#Layout
app.layout = html.Div(style={"backgroundColor": colors["background"]}, children=[

    dcc.Interval(
    id = "interval",
    interval = 120 * 1000,      #milliseconds 
    n_intervals = 0

    ),

    dcc.Store(id = "data_store"),

    html.H1(
        children= "Biomonitoring Dashboard",
        style={
            "textAlign": "center",
            "color": colors["text"]
        }
    ),

    html.Div(children= ["A web application framework for your data.", 
        dcc.Markdown("""For more information visit [biomoni](https://github.com/PSenck/biomoni)""")     #htlm.A geht auch für link
        ], style={
        "textAlign": "center",
        "color": colors["text"]
    }),

    html.Br(),

    html.Div([
        
        html.Div([
            html.Div("Displayed variables of measurement data", style =  {"color" : colors["text"]}),
            dcc.Dropdown(
                id='meas_vars',
                options=[{'label': i, 'value': i} for i in measurement_vars],
                value = measurement_vars ,
                multi = True,
        
            ),
            html.Div("Displayed variables of simulated data", style =  {"color" : colors["text"]}),
            dcc.Dropdown(
                id='sim_vars',
                options=[{'label': i, 'value': i} for i in simulated_vars],
                value = [],
                multi = True,
        
            ),
            
            dcc.RadioItems(
                id='yaxis_type',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='linear',
                labelStyle={'display': 'inline-block'},
                style = {"color" : colors["text"]},
                
                
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.Div("Variables to be displayed on the secondary_yaxis", style =  {"color" : colors["text"]}),
            dcc.Dropdown(
                id='secondary_yaxis',
                options=[{'label': i, 'value': i} for i in all_vars],
                value =  [],
                multi = True
            ),
        

            dcc.RadioItems(
                id='secondary_yaxis_type',
                options=[{'label': i, 'value': i} for i in ['linear', 'log']],
                value='linear',
                labelStyle={'display': 'inline-block'},
                style = {"color" : colors["text"]}
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style = {"backgroundColor" : colors["settings"]}),

    dcc.Graph(
        id = "graph1",
        figure={} 

    ),

    html.Div([
        html.Div("Simulation time in hours: ", style =  {"color" : colors["text"]}),
        dcc.Input(id= "sim_time", value= 10, type='number'),
    ], style = {"backgroundColor" : colors["settings"]}),

    html.Div([

        html.Div([
            html.Div("Manual parameter estimation", style =  {"color" : colors["text"]}),
            html.Button(id="button_id", children="Estimate!"),
            html.Div([html.P(id="paragraph_id", children=["Button not clicked"])]),

    ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Div("Automatic parameter estimation", style =  {"color" : colors["text"]}),
            dcc.RadioItems(
                id= "automatic_parest",
                options=[{'label': i, 'value': i} for i in ['enabled', 'disabled']],
                value= "enabled",
                labelStyle={'display': 'inline-block'},
                style = {"color" : colors["text"]} )

        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        
    ], style = {"backgroundColor" : colors["settings"]}),
    

    dash_table.DataTable(
        id="table_params",
        columns= [],             
        data= [],     
        style_header={
        "color" : colors["text"],
        'backgroundColor': colors["table_background"],
        'fontWeight': 'bold'},
    ),

    html.Div("This is before any iterations of dcc.Interval", id = "iteration_identifier")

])


@app.callback(
    Output("graph1", "figure"),
    Output("secondary_yaxis", "options"),
    Input("data_store", "data"),
    Input("meas_vars", "value"),
    Input("sim_vars", "value"),
    Input("secondary_yaxis", "value"),
    Input("yaxis_type", "value"),
    Input("secondary_yaxis_type", "value"))
def update_graph_1(jsonified_data, meas_vars, sim_vars, secondary_yaxis, yaxis_type, secondary_yaxis_type):
    """Function to update the graph with data from the store, it is possible to change the graph by choosing which columns of the data should be displayed, on which axis it should be displayed and if it should be displayed in logarithmic mode"""
    if jsonified_data is not None:
        
        dataset = json.loads(jsonified_data)
        simulated_data = pd.read_json(dataset["simulated_data"], orient = "split").rename_axis("t")
        simulated_data = simulated_data.filter(items = sim_vars)
        measured_data = {}
        cols_measured = []
        for typ, dat in dataset["measured_data"].items():
            measured_data[typ] = pd.read_json(dat, orient = "split").rename_axis("t")
            filter_cols = [col for col in  measured_data[typ].columns if col in meas_vars]
            measured_data[typ] = measured_data[typ].filter(items = filter_cols)
            [cols_measured.append(i) for i in list(measured_data[typ].columns)]

        
        fig = visualize(measured_data, simulated_data,  secondary_y_cols= secondary_yaxis, yaxis_type = yaxis_type, sec_yaxis_type = secondary_yaxis_type )

        all_columns = set(cols_measured + list(simulated_data.columns))
        options_sec_y=[{'label': i, 'value': i} for i in all_columns]

    else:
        fig = {}
        options_sec_y = [{'label': i, 'value': i} for i in all_vars]
    
    
    return fig, options_sec_y

@app.callback(
    Output("table_params", "columns"),
    Output("table_params", "data"),
    Output("table_params", "dropdown"),
    Input("data_store", "data"),
)
def update_table_params(jsonified_data):
    """Function to update the DataTable with data from the store"""
    dataset = json.loads(jsonified_data)
    params = dataset["params"]
    params = pd.DataFrame(params).T
    col_names = []
    for col in params.columns:
        editable_flag = col in ["vary", "min", "max", "value"]
        column_type = "numeric" if col not in ["vary", "name"] else "text" 
        #presentation = "dropdown" if col in ["vary"] else None
        if col in ["vary"]:
            dic = {"name": col, "id": col, "editable" : editable_flag, "type": column_type, "format" : Format(precision=5), "presentation": "dropdown"}    #, 'presentation': 'dropdown'
        else: 
            dic = {"name": col, "id": col, "editable" : editable_flag, "type": column_type, "format" : Format(precision=5)}
        
        dropdown={
            'vary': {
                'options': [
                    {'label': str(i), 'value': str(i)}
                    for i in params['vary'].unique()
                ]
            , "clearable" : False } }        
        col_names.append(dic)


    return col_names, params.to_dict("records"), dropdown


@app.callback(
Output("data_store", "data"),
Output("iteration_identifier", "children"),
Output("paragraph_id", "children"),
Input("interval", "n_intervals"),
Input("sim_time", "value"),
Input("button_id", "n_clicks"),
State("automatic_parest", "value"),
State("table_params", "data"),
State("table_params", "columns"),
running=[
    (Output("button_id", "disabled"), True, False),
    (Output("callback_check", "children"), "callback is currently running", "callback is not running")
],
)
def create_data(n_intervals, hours, n_clicks, parest_mode, data, columns):
    ctx = dash.callback_context
    last_input = ctx.triggered[0]["prop_id"].split(".")[0]
    print(last_input)

    if last_input == "":
        Exp = deepcopy(Exp_init)
        y = deepcopy(y_init)
        print("Initial callback was executed")

    if last_input != '':
        Exp = Exp_class(path, **experiment_options)
        y = model_class()
        params = pd.DataFrame(data, columns=[c['name'] for c in columns]).set_index("name")
        for p, row in params.iterrows():
            if row["vary"] in ["True", "true"]: 
                row["vary"] = True
            elif row["vary"] in ["False", "false"]:
                row["vary"] = False

            y.change_params(p, vary= row["vary"], value= row["value"], min= row["min"], max= row["max"])

        if last_input == "interval":
            if parest_mode == "enabled":
                print("Automatic parameter estimation")
                y.estimate(Exp, **estimation_options)
        

        elif last_input == "button_id":
            y.estimate(Exp, **estimation_options)
        
    
    t_grid = np.linspace(0,hours, round(hours*60)) 
    sim = y.simulate(Exp, t_grid = t_grid)
        
    dataset = Exp.dataset
    p_dict = {}
    for p, val in y.p.items():
        p_dict[p] = {
            "name": val.name,
            "value": val.value,
            "vary": str(val.vary),      #str because json converts boolen True to string true, there 
            "min" : val.min,
            "max" : val.max,
            }

    dataset = {}
    for typ, df in Exp.dataset.items():
        dataset[typ] = df.to_json(orient = "split", date_format = "iso")
    
    all_data = {
    "measured_data" : dataset,
    "simulated_data" : sim.to_json(orient = "split", date_format = "iso"),
    "params" : p_dict
    }
    iteration_nr = "This is iteration: " + str(n_intervals)

    return json.dumps(all_data), iteration_nr, [f"Clicked {n_clicks} times"]


if __name__ == "__main__":
    app.run_server(host='localhost' , port="7777",  dev_tools_hot_reload=False, debug = True)     #debug=True, host='localhost' , host="0.0.0.0"

# visit http://localhost:7777/ in your web browser.


#sqlite3.DatabaseError: database disk image is malformed

