import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/relationship', name="Relationship 📈")

####################### DATASET #############################
# Load your dataset
titanic_df = pd.read_csv("bank.csv")

####################### SCATTER CHART (With Markers and Lines) #############################
def create_scatter_chart(x_axis="Quick Ratio", y_axis="Current Ratio"):
    fig = px.scatter(data_frame=titanic_df, x=x_axis, y=y_axis, height=600)
    fig.update_traces(mode='lines+markers')  # Show both points and lines
    return fig

####################### WIDGETS #############################
# Use the correct column names from the dataset
columns = [{"label": col, "value": col} for col in titanic_df.columns]  # Dynamically generate dropdown options

x_axis = dcc.Dropdown(id="x_axis", options=columns, value=titanic_df.columns[0], clearable=False)
y_axis = dcc.Dropdown(id="y_axis", options=columns, value=titanic_df.columns[1], clearable=False)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.Label("X-Axis"), x_axis,
    html.Label("Y-Axis"), y_axis,
    dcc.Graph(id="scatter")
])

####################### CALLBACKS ###############################
@callback(
    Output("scatter", "figure"), 
    [Input("x_axis", "value"), Input("y_axis", "value")]
)
def update_scatter_chart(x_axis, y_axis):
    # Generate the scatter chart with the selected axes
    return create_scatter_chart(x_axis, y_axis)
