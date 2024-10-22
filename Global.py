import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
df = pd.read_csv(url)

# Initialize the Dash app
app = dash.Dash(__name__)
server=app.server

# App layout
app.layout = html.Div(style={'backgroundColor': 'black', 'color': 'white', 'padding': '20px', 'height': '100vh'}, children=[
    html.H1("Global Insights: GDP and Life Expectancy Trends", style={'text-align': 'center'}),
    dcc.Dropdown(id='country-dropdown', 
                 options=[{'label': country, 'value': country} for country in df['country'].unique()],
                 value='United States', multi=False, 
                 style={'width': '50%', 'margin': 'auto', 'color': 'black'}),
    html.Div(style={'display': 'flex', 'justify-content': 'space-around', 'flex-direction': 'column', 'height': '80%'}, children=[
        dcc.Graph(id='gdp-lifeexp-pie', style={'height': '50%'}),
        html.Div(style={'display': 'flex', 'flex-direction': 'row', 'width': '100%', 'height': '50%'}, children=[
            dcc.Graph(id='gdp-over-time', style={'height': '100%', 'width': '50%'}),
            dcc.Graph(id='life-exp-over-time', style={'height': '100%', 'width': '50%'})
        ])
    ])
])

# Callbacks for interactivity
@app.callback(
    Output('gdp-lifeexp-pie', 'figure'),
    Output('gdp-over-time', 'figure'),
    Output('life-exp-over-time', 'figure'),
    Input('country-dropdown', 'value')
)
def update_graphs(selected_country):
    filtered_df = df[df['country'] == selected_country]

    pie_chart = px.pie(names=['GDP per Capita', 'Life Expectancy'],
                        values=[filtered_df['gdpPercap'].iloc[0], filtered_df['lifeExp'].iloc[0]],
                        title=f'GDP and Life Expectancy - {selected_country}')
    pie_chart.update_layout(paper_bgcolor='black', plot_bgcolor='black', font_color='white')

    gdp_over_time = {
        'data': [{'x': filtered_df['year'], 'y': filtered_df['gdpPercap'], 'type': 'scatter', 'mode': 'lines+markers',
                  'name': selected_country}],
        'layout': {'title': f'GDP Over Time - {selected_country}', 
                   'xaxis': {'title': 'Year', 'gridcolor': 'gray'},
                   'yaxis': {'title': 'GDP per Capita', 'gridcolor': 'gray'}, 
                   'paper_bgcolor': 'black', 'plot_bgcolor': 'black', 
                   'font': {'color': 'white'}, 'xaxis': {'showgrid': False}, 
                   'yaxis': {'showgrid': False}}
    }

    life_exp_over_time = {
        'data': [{'x': filtered_df['year'], 'y': filtered_df['lifeExp'], 'type': 'bar',
                  'name': selected_country}],
        'layout': {'title': f'Life Expectancy Over Time - {selected_country}', 
                   'xaxis': {'title': 'Year', 'gridcolor': 'gray'},
                   'yaxis': {'title': 'Life Expectancy', 'gridcolor': 'gray'}, 
                   'paper_bgcolor': 'black', 'plot_bgcolor': 'black', 
                   'font': {'color': 'white'}, 'xaxis': {'showgrid': False}, 
                   'yaxis': {'showgrid': False}}
    }

    return pie_chart, gdp_over_time, life_exp_over_time

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
