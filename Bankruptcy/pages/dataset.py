import pandas as pd
import dash
from dash import html, dash_table, dcc, callback, Input, Output, State
import base64
import io

dash.register_page(__name__, path='/dataset', name="Dataset 📋")

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    
    # File upload component
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a CSV File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # Single file upload
    ),
    
    # Output DataTable to show the uploaded CSV
    dash_table.DataTable(id='table-data', page_size=20,
                         style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left"},
                         style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"},
                        ),
])

####################### CALLBACKS ###############################
@callback(
    Output('table-data', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_table(contents, filename):
    if contents is None:
        return []

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Read CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df.to_dict('records')
        else:
            return []
    except Exception as e:
        return []

