import numpy as np
import pandas as pd
import plotly.graph_objs as go
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output

# Bootstrap CSS and JS
BOOTSTRAP_CSS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
BOOTSTRAP_JS = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[BOOTSTRAP_CSS], external_scripts=[BOOTSTRAP_JS])

# Load dataset
try:
    patients = pd.read_csv("./Dataset/IndividualDetails.csv")
except FileNotFoundError:
    print("Error: Dataset file not found!")
    patients = pd.DataFrame(columns=['detected_state', 'current_status'])  # Avoid breaking

# Compute state-wise summary
statewise_counts = (
    patients.groupby('detected_state')['current_status']
    .value_counts()
    .unstack(fill_value=0)
    .reset_index()
)
# Summary statistics
total = patients.shape[0]
active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
deaths = patients[patients['current_status'] == 'Deceased'].shape[0]
# Add total cases column
statewise_counts['Total'] = (
    statewise_counts.get('Hospitalized', 0) +
    statewise_counts.get('Recovered', 0) +
    statewise_counts.get('Deceased', 0)
)
options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},  # Fixed typo
    {'label': 'Deceased', 'value': 'Deceased'}
]

# Get unique states for dropdown
state_options = [{'label': state, 'value': state} for state in statewise_counts['detected_state']]
state_options.insert(0, {'label': 'All States', 'value': 'All'})

# App Layout
app.layout = html.Div([
    html.H1("Corona Virus Pandemic", style={"text-align": "center", "color": "#ffff"}),

    # Summary Cards
    html.Div(className='row p-4', children=[
        html.Div(className='col-md-3 mb-6', children=[
            html.Div(className='card bg-danger text-light', children=[
                html.Div(className='card-body', children=[
                    html.H3("Total Cases"),
                    html.H4(total)
                ])
            ])
        ]),

        html.Div(className='col-md-3', children=[
            html.Div(className='card bg-success text-light', children=[
                html.Div(className='card-body', children=[
                    html.H3("Recovered Cases"),
                    html.H4(recovered)
                ])
            ])
        ]),
        html.Div(className='col-md-3', children=[
            html.Div(className='card bg-warning text-light', children=[
                html.Div(className='card-body', children=[
                    html.H3("Active Cases"),
                    html.H4(active)
                ])
            ])
        ]),
        html.Div(className='col-md-3', children=[
            html.Div(className='card bg-dark text-light', children=[
                html.Div(className='card-body', children=[
                    html.H3("Deaths"),
                    html.H4(deaths)
                ])
            ])
        ]),
 # Dropdown and Graph
        html.Div(className='row mt-5 p-4', children=[
            html.Div(className='col-md-12', children=[
                html.Div(className='card', children=[
                    html.Div(className='card-body', children=[
                        dcc.Dropdown(id="picker", options=options, value='All'),
                        dcc.Graph(id='bar')
                    ])
                ])
            ])
        ])
    ]),


    # Dropdown to select a state
    html.Div([
        dcc.Dropdown(id="state_picker", options=state_options, value='All', clearable=False),
    ], className="mb-4 p-2"),

    # Table to show state-wise data
    dash_table.DataTable(
        id='statewise_table',
        columns=[
            {'name': 'State', 'id': 'detected_state'},
            {'name': 'Total Cases', 'id': 'Total'},
            {'name': 'Active Cases', 'id': 'Hospitalized'},
            {'name': 'Recovered Cases', 'id': 'Recovered'},
            {'name': 'Deaths', 'id': 'Deceased'}
        ],
        data=statewise_counts.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_header={'fontWeight': 'bold', 'backgroundColor': '#f1f1f1'}
    ),

    # Bar Chart
    dcc.Graph(id='statewise_bar_chart'),
])


# Callback to update table and graph
@app.callback(
    [Output('statewise_table', 'data'),
     Output('statewise_bar_chart', 'figure')],
    [Input('state_picker', 'value')]
)
def update_statewise_data(selected_state):
    if selected_state == 'All':
        filtered_data = statewise_counts
    else:
        filtered_data = statewise_counts[statewise_counts['detected_state'] == selected_state]

    # Convert to dictionary format for table
    table_data = filtered_data.to_dict('records')

    # Bar chart data
    figure = {
        'data': [
            go.Bar(x=filtered_data['detected_state'], y=filtered_data['Total'], name="Total Cases"),
            go.Bar(x=filtered_data['detected_state'], y=filtered_data['Hospitalized'], name="Active Cases", marker_color='orange'),
            go.Bar(x=filtered_data['detected_state'], y=filtered_data['Recovered'], name="Recovered Cases", marker_color='green'),
            go.Bar(x=filtered_data['detected_state'], y=filtered_data['Deceased'], name="Deaths", marker_color='red'),
        ],
        'layout': go.Layout(
            title="State-wise COVID-19 Cases",
            barmode="stack",
            xaxis={'title': 'State'},
            yaxis={'title': 'Cases'},
            legend={'title': 'Case Type'}
        )
    }

    return table_data, figure

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
