import numpy as np
import pandas as pd
import plotly.graph_objs as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Bootstrap CSS
BOOTSTRAP_CSS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[BOOTSTRAP_CSS])

# Load dataset
try:
    patients = pd.read_csv("./Dataset/IndividualDetails.csv")
except FileNotFoundError:
    print("Error: Dataset file not found!")
    patients = pd.DataFrame(columns=['detected_state', 'current_status'])  # Avoid breaking

# Summary statistics
total = patients.shape[0]
active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
deaths = patients[patients['current_status'] == 'Deceased'].shape[0]

# Dropdown options
options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},  # Fixed typo
    {'label': 'Deceased', 'value': 'Deceased'}
]

# App layout
app.layout = html.Div([
    html.H1("Corona Virus Pandemic", style={
        "text-align": "center",
        "color": "#F9F9F9",
        "font-family": "Poppins, sans-serif",
        "font-size": "36px"
    }),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className='text-light'),
                    html.H4(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered Cases", className='text-light'),
                    html.H4(recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className='text-light'),
                    html.H4(active, className='text-light')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-3'),

        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths", className='text-light'),
                    html.H4(deaths, className='text-light')
                ], className='card-body')
            ], className='card bg-dark')
        ], className='col-md-3')
    ], className='row mb-4'),

    html.Div([
        html.Div([], className='col-md-6'),
        html.Div([], className='col-md-6')
    ], className='row'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id="picker", options=options, value='All'),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row')

], className='container p-4')


# Callback function
@app.callback(Output('bar', 'figure'), [Input('picker', 'value')])
def update_graph(case_type):
    if case_type == 'All':
        pbar = patients['detected_state'].value_counts().reset_index()
    else:
        npat = patients[patients['current_status'] == case_type]
        pbar = npat['detected_state'].value_counts().reset_index()

    # Rename columns properly
    pbar.columns = ['state', 'count']

    return {
        'data': [go.Bar(x=pbar['state'], y=pbar['count'])],
        'layout': go.Layout(title='State Total Cases')
    }


# Run server
if __name__ == "__main__":
    app.run_server(debug=True)
