import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/distribution', name="Distribution 📊")

####################### LOAD DATASET #############################
# Load your dataset (ensure it has correct column names)
titanic_df = pd.read_csv("bank.csv")

####################### HISTOGRAM ###############################
def create_distribution(col_name):
    return px.histogram(data_frame=titanic_df, x=col_name, height=600)

####################### WIDGETS ################################
# Use the correct column names from the dataset for dropdown options
columns = [{"label": col, "value": col} for col in titanic_df.columns]
dd = dcc.Dropdown(id="dist_column", options=columns, value=titanic_df.columns[0], clearable=False)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.P("Select Column:"),
    dd,
    dcc.Graph(id="histogram")
])

####################### CALLBACKS ################################
@callback(
    Output("histogram", "figure"),
    [Input("dist_column", "value")]
)
def update_histogram(dist_column):
    # Return the histogram using the selected column
    return create_distribution(dist_column)
