import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/survived', name="Bankrupt📊")

####################### DATASET #############################
titanic_df = pd.read_csv("bank.csv")

####################### BAR CHART #############################
def create_bar_chart(col_name="Bankrupt"):
    fig =  px.histogram(data_frame=titanic_df, x="Bankrupt", color=col_name,
                        histfunc="count", barmode='group', height=600)
    fig = fig.update_layout(bargap=0.5)
    return fig

####################### WIDGETS ################################
columns = ["Bankrupt"]
dd = dcc.Dropdown(id="sel_col", options=columns, value="Bankrupt", clearable=False)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    dd, 
    dcc.Graph(id="bar_chart")
])

####################### CALLBACKS ################################
@callback(Output("bar_chart", "figure"), [Input("sel_col", "value"), ])
def update_bar_chart(sel_col):
    return create_bar_chart(sel_col)