
from biomoni import Experiment, Yeast
from biomoni import visualize
from biomoni.file_manager import pull_azure_file


import numpy as np
import pandas as pd

import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Format
from dash.dependencies import Input, Output, State
from settings_dash import kwargs_experiment, kwargs_estimate, Variables

import json


#download data from Azure
connection_string = "DefaultEndpointsProtocol=https;AccountName=biomonistorage;AccountKey=hwA0oCscA7HbTxYvkyainLR/5WrVk3lBkfsiCTJEbQCTAur5BHddOVnRxJlgt0iSxqxufqBmQUZvGCk3epXXBQ==;EndpointSuffix=core.windows.net"
share_name = "biomoni-storage"
azure_exp_file_path = "Measurement-data/current_ferm/data.csv" 
azure_metadata_file_path = "Measurement-data/metadata_OPCUA.ods"
[pull_azure_file(connection_string= connection_string, share_name= share_name, azure_file_path= i) for i in [azure_exp_file_path, azure_metadata_file_path]]



#select your variables to be displayed
measurement_vars = Variables["typ1"]["measurement_vars"]        #typ2
simulated_vars = Variables["typ1"]["simulated_vars"]

#This code block are asignments, in order to work with your individual data, use your Experiment class and the respective options to run their constructors
Exp_class = Experiment      #assign your Experiment class to Exp_class
model_class = Yeast         #assign your Model class to model_class
experiment_options = kwargs_experiment["typ1"]       #use ur options to create an Experiment
estimation_options = kwargs_estimate["typ1"]         #use ur options to estimate

#Using on, off, CO2 data from F7
path = "Measurement-data"


all_vars = set([*measurement_vars, *simulated_vars])    #All variables only once, used to display the options in the dropdown at the initial callback

#color dict to style your layout
colors = {
    "background": "oxy",
    "text": "green",
    "settings" : "lightyellow",
    "table_header" : "red",
    "table_background" : "grey"
}


#Create dash app
dash_app = dash.Dash(__name__)     #external_stylesheets = external_stylesheets      #, long_callback_manager = long_callback_manager
app = dash_app.server

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
dash_app.layout = html.Div(style={"backgroundColor": colors["background"]}, children=[

    html.Div(id = "Error_div", children = [
        html.H2("Something went wrong, an error occurred within the 'create_data' callback with the following description:"),
        html.Div(children = [], id = "Errormessage"),
        html.Button(id="button_error", children="Try again", style = {"color": colors["text"],"backgroundColor" : colors["settings"]}),
        html.P(id="error_clicks", children=["Button not clicked"], style = {"color": colors["text"],"backgroundColor" : colors["settings"]}),
    ], style = {"display" : "None", "textAlign": "center", "backgroundColor" : colors["settings"]} ),

    html.Div(id = "layout", children = [
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
            #dcc.Markdown("""For more information visit [biomoni](https://github.com/PSenck/biomoni)""")     #htlm.A geht auch für link
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
        html.Button(id = "options_button", children = "Show options", style={'display': 'inline-block', 'vertical-align': 'middle',"min-width": "150px",
            'height': "25px",
            "margin-top": "0px",
            "margin-left": "5px",
            "color": colors["text"],
            "backgroundColor" : colors["settings"]}),
        ], style = {"textAlign": "center"}),


        html.Div(id = "options_div", children = [
            html.Div([
                html.Div("Simulation time in hours: ", style =  {"color" : colors["text"]}),
                dcc.Input(id= "sim_time", value= 10, type='number'),
            ], style = {"backgroundColor" : colors["settings"], "margin-bottom": "30px"}),

            html.Div([

                html.Div([
                    html.Div("Manual parameter estimation", style =  {"color" : colors["text"], "margin-bottom": "10px"}),
                    html.Button(id="button_id", children="Estimate!", style = {"color": colors["text"],"backgroundColor" : colors["settings"]}),
                    html.Div([html.P(id="paragraph_id", children=["Button not clicked"], style = {"color": colors["text"],"backgroundColor" : colors["settings"]})]),

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
        ], style = {}),
        ], style = {})
])



@dash_app.callback(
    Output("layout", "style"),
    Output("Error_div", "style"),
    Input("Errormessage", "children")
)
def change_layout(Errormessage):
    
    if Errormessage == "None":
        layout_style = {}
        message_style = {"display" : "None", "textAlign": "center", "backgroundColor" : colors["settings"]}
    else:
        layout_style = {"display" : "None"}
        message_style = {"textAlign": "center", "backgroundColor" : colors["settings"]}
    return layout_style, message_style

@dash_app.callback(
    Output("options_button", "children"),
    Output("options_div", "style"),
    Input("options_button", "n_clicks")
)
def show_options(n_clicks):

    if n_clicks is None or (n_clicks % 2) == 0 or n_clicks == 0:
        button_text = "Show options"
        style = {"display" : "None"}
    else:
        button_text = "Hide options"
        style = {"backgroundColor" : colors["settings"]}
    
    return button_text, style

@dash_app.callback(
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
    
    if jsonified_data is not None and json.loads(jsonified_data)["measured_data"]:
        
        data = json.loads(jsonified_data)
        simulated_data = pd.read_json(data["simulated_data"], orient = "split").rename_axis("t")
        simulated_data = simulated_data.filter(items = sim_vars)
        measured_data = {}
        cols_measured = []
        for typ, dat in data["measured_data"].items():
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

@dash_app.callback(
    Output("table_params", "columns"),
    Output("table_params", "data"),
    Output("table_params", "dropdown"),
    Input("data_store", "data"),
)
def update_table_params(jsonified_data):
    """Function to update the DataTable with data from the store"""
    data = json.loads(jsonified_data)
    params = data["params"]
    if params:      #check if list is empty
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
    else:
        return [], [], {}
    


@dash_app.callback(
Output("data_store", "data"),
Output("iteration_identifier", "children"),
Output("paragraph_id", "children"),
Output("error_clicks", "children"),
Output("Errormessage", "children"),
Input("interval", "n_intervals"),
Input("sim_time", "value"),
Input("button_id", "n_clicks"),
Input("button_error", "n_clicks"),
State("automatic_parest", "value"),
State("table_params", "data"),
State("table_params", "columns"),
State("Errormessage", "children"),
running=[
    (Output("button_id", "disabled"), True, False),
    (Output("callback_check", "children"), "callback is currently running", "callback is not running")
],
)
def create_data(n_intervals, hours, n_clicks, n_clicks_error, parest_mode, data, columns, Errormessage):
    ctx = dash.callback_context
    last_input = ctx.triggered[0]["prop_id"].split(".")[0]
    print(last_input)
    iteration_nr = "This is iteration: " + str(n_intervals)
    

    if last_input == "" or last_input == "button_error" or Errormessage != "None":        #
        pull_azure_file(connection_string= connection_string, share_name= share_name, azure_file_path= azure_exp_file_path)
        try:
            Exp = Exp_class(path, **experiment_options)
            y = model_class()
            y.estimate(Exp, **estimation_options)
            Errormessage = None
        except Exception as ex:
            Errormessage = ex


    elif last_input != '':
        try:
            pull_azure_file(connection_string= connection_string, share_name= share_name, azure_file_path= azure_exp_file_path)
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

            Errormessage = None

        except Exception as ex:
            Errormessage= ex
        
    if Errormessage is None:
        t_grid = np.linspace(0,hours, round(hours*60)) 
        sim = y.simulate(Exp, t_grid = t_grid)
            
        #dataset = Exp.dataset
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

        
    elif Errormessage is not None:

        all_data ={
        "measured_data" : {},
        "simulated_data" : {},
        "params" : {}
        }


    return json.dumps(all_data), iteration_nr, [f"Clicked {n_clicks} times"], [f"Clicked {n_clicks_error} times"], str(Errormessage)


if __name__ == "__main__":
    dash_app.run_server(debug = True, host='0.0.0.0', port='8000')     #debug=True, host='localhost' , host="0.0.0.0"

# visit http://localhost:7777/ in your web browser.


#sqlite3.DatabaseError: database disk image is malformed

