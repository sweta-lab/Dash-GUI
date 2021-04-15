import plotly_express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import timedelta, datetime

def obtain_stress_report(starting_time, stress_scores , threshold_bounds,
                         heart_rate, step_count, sleep_stages):
   
   
    def SetColor(x):
        if(x <= threshold_bounds[1]):
            return "green"
        elif(x <= threshold_bounds[2]):
            return "blue"
        elif(x <= threshold_bounds[3]):
            return "yellow"
        elif(x <= threshold_bounds[4]):
            return "red"
        elif(x > 1):
            return "black"
   
    ###### Combine all the data into one dataframe

    data = pd.merge(heart_rate, stress_scores,on = heart_rate.index)
    data.columns = ['Time', 'Heart Rate', 'Stress Scores']
    data1= pd.merge(step_count, sleep_stages, on=step_count.index)
    data1.columns=['Time', 'Step Count', 'Sleep Stages']

    
    ######Time stamps array
    starting_time=0
    starting_time = datetime.fromtimestamp(starting_time / 1e3)
    start_time = [starting_time + timedelta(hours=i ) for i in range(0, 50, 1)]
   
    #Dropdown options
   
    col_options = [dict(label = x, value = x) for x in {'Stress Scores', 'Sleep Stages', 'Step Count',
                                                        'Heart Rate', }]
    dimensions = ["Select Graph"]
    number=5

    app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    )
   
    app.layout = html.Div(
    [
        dbc.Row(
            [
            html.H1("STRESS REPORT")
            ], style={'text-align':'center'},
            ),
        dbc.Row(
            [dbc.Col(html.Div([
            html.P([d + ":", dcc.Dropdown(id=d, options=col_options, searchable=True, optionHeight= 45 )])
            for d in dimensions],
            style={"width": "25%", "float": "left"},
                            )),
            dcc.Graph(id="graph", style={"width": "65%", "height": "40%", 'float':'right'}),
           
            html.Div([dcc.Markdown('''*Percentage duration of high stress: %d %s*''' %(number,'%' ))],
                             style ={"width": "30%", "float": "left", 'font-size': '130%', 'marginTop': '15%',
                                     'text-align':'center', 'border': 'solid', 'padding': '6px 0px 0px 8px'},
                             )]),
        ])
    template= 'seaborn'
   
    #Add callback to change the graph based on dropdown value
    @app.callback(Output("graph", "figure"), [Input(d, "value") for d in dimensions])
    def update_graph(y):
        fig = []
        if y == "Stress Scores" or not y:
            fig = px.bar(data, x= data['Time'], y = data['Stress Scores'])
            fig.update_layout(height = 540, width = 900, title_text = "<b>Stress Scores</b>", title_x = 0.5)
            fig.update_yaxes(title_text = "Stress Scores")
            fig.update_xaxes(title_text = "Time(HH:MM)")
            
            fig.update_xaxes(showline=True, linewidth=3, linecolor='black', mirror=True,
                          ticktext= [start_time[i].strftime("%H:%M") for i in range(0, len(start_time), 10)],
                          tickvals=[(i) for i in range(0, len(data['Stress Scores']), 10)],
                          tickson = "boundaries",
                          ticks = 'outside', ticklen = 20, tickcolor='crimson', tickangle= 0)
            fig.update_yaxes(showline=True, linewidth=3, linecolor='black', mirror=True)

           
        elif y == "Sleep Stages":
           
            fig = px.bar(data1, x= data1['Time'], y = data1['Sleep Stages'])
            fig.update_layout(height = 540, width = 900, title_text = "<b>Sleep Stages</b>", title_x = 0.5)
            
            fig.update_xaxes(showline=True, linewidth=3, linecolor='black', mirror=True,
                          ticktext= [start_time[i].strftime("%H:%M") for i in range(0, len(start_time), 10)],
                          tickvals=[(i) for i in range(0, len(data1['Sleep Stages']), 10)],
                          tickson = "boundaries",
                          ticks = 'outside', ticklen = 20, tickcolor='crimson', tickangle= 0,
                          title_text="Sleep Stages")
            fig.update_yaxes(showline=True, linewidth=3, linecolor='black', mirror=True, title_text="Time (HH:MM)")
            
            
        
        elif y == "Step Count":
            fig = px.line(data1, x = data1['Time'], y = data1['Step Count'],
                                title = "<b>Step Count</b>",
                                height = 540,
                                template = template
                                )
           
            fig.update_layout(height = 540, width = 900, title_text = "<b>Step Count</b>", title_x = 0.5)
            fig.update_yaxes(title_text = "Step Count")
            fig.update_xaxes(title_text = "Time(HH:MM)")
            
            fig.update_xaxes(showline=True, linewidth=3, linecolor='black', mirror=True,
                          ticktext= [start_time[i].strftime("%H:%M") for i in range(0, len(start_time), 10)],
                          tickvals=[(i) for i in range(0, len(data1['Step Count']), 10)],
                          tickson = "boundaries",
                          ticks = 'outside', ticklen = 20, tickcolor='crimson', tickangle= 0)
            fig.update_yaxes(showline=True, linewidth=3, linecolor='black', mirror=True)

        elif y =="Heart Rate":
            fig = px.line(data, x = data['Time'], y = data['Heart Rate'],
                                title = "<b>Heart Rate</b>",
                                height = 540,
                                template = template
                                )
            fig.update_layout(height = 540, width = 900, title_text = "<b>Heart Rate</b>", title_x = 0.5)
            fig.update_yaxes(title_text = "Heart Rate")
            fig.update_xaxes(title_text = "Time(HH:MM)")
            
            fig.update_xaxes(showline=True, linewidth=3, linecolor='black', mirror=True,
                          ticktext= [start_time[i].strftime("%H:%M") for i in range(0, len(start_time), 10)],
                          tickvals=[(i) for i in range(0, len(data['Heart Rate']), 10)],
                          tickson = "boundaries",
                          ticks = 'outside', ticklen = 20, tickcolor='crimson', tickangle= 0)
            fig.update_yaxes(showline=True, linewidth=3, linecolor='black', mirror=True)
             

             
        return fig
           
    return app

if __name__=="__main__":
    threshold_bounds=[0,1,2,4,5,6]
    heart_rate=pd.DataFrame(np.random.randint(0, 5, 50))
    stress_scores=pd.DataFrame(np.random.randint(0, 5, 50))
    sleep_stages=pd.DataFrame(np.random.randint(0, 5, 50))
    step_count=pd.DataFrame(np.random.randint(0, 5, 50))
    starting_time=0
    app = obtain_stress_report(starting_time, stress_scores, threshold_bounds, heart_rate, step_count, sleep_stages)
    app.run_server(debug=False)

