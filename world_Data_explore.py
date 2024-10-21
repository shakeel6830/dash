# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

# Initialize the app
app = Dash()

# Get a list of countries for the dropdown
countries = df['country'].unique()

# App layout
app.layout = html.Div(style={
    'backgroundColor': '#2c3e50',  # Dark background
    'color': 'white',
    'padding': '20px',
    'fontFamily': 'Arial, sans-serif'
}, children=[
    html.Div(children='World Data Explorer: Visualizing Trends by Country',
             style={
                 'textTransform': 'uppercase',
                 'textAlign': 'center',
                 'fontSize': '28px',
                 'marginBottom': '20px'
             }),
    html.Hr(style={'borderColor': '#ecf0f1'}),
    
    dcc.Dropdown(
        options=[{'label': country, 'value': country} for country in countries],
        value=countries[0],
        id='country-dropdown',
        style={
            'backgroundColor': '#ecf0f1',
            'color': 'black',
            'border': '1px solid #bdc3c7',
            'marginBottom': '20px'
        }
    ),
    
    dcc.RadioItems(
        options=[
            {'label': 'Population', 'value': 'pop'},
            {'label': 'Life Expectancy', 'value': 'lifeExp'},
            {'label': 'GDP per Capita', 'value': 'gdpPercap'}
        ],
        value='pop',
        id='controls-and-radio-item',
        style={
            'color': 'white',
            'marginBottom': '20px'
        }
    ),
    
    dash_table.DataTable(
        id='country-data-table',  # Added ID for callback reference
        page_size=6,
        style_table={'overflowX': 'auto'},
        style_header={
            'backgroundColor': '#3498db',  # Blue header
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_cell={
            'backgroundColor': '#ecf0f1',  # Light gray cells
            'color': 'black',
            'border': '1px solid #bdc3c7'
        },
    ),
    
    dcc.Graph(figure={}, id='controls-and-graph', style={'height': '60vh'})
])

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Output(component_id='country-data-table', component_property='data'),  # Output for table data
    Input(component_id='country-dropdown', component_property='value'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(selected_country, selected_metric):
    filtered_df = df[df['country'] == selected_country]
    
    # Update the graph
    fig = px.bar(filtered_df, x='year', y=selected_metric, title=f'{selected_metric.capitalize()} over Years for {selected_country}',labels={"pop":"population"})
    fig.update_layout(plot_bgcolor='lightgray')  # Set plot background to whitish gray
    
    # Return the filtered data for the table
    return fig, filtered_df.to_dict('records')  # Return figure and filtered data

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
