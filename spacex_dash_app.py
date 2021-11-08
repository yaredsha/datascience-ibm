# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# dynamic lauch site options
launch_sites = spacex_df['Launch Site'].unique()
launch_sites_options = launch_sites.tolist()
launch_sites_options.insert(0, 'ALL')

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=[{'label':name, 'value':name} for name in launch_sites_options],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data_all = spacex_df[spacex_df['class'] != 0]
        data_all = data_all.groupby(['Launch Site']).size().reset_index(name='class')
        fig = px.pie(data_all, values='class', names='Launch Site', title='Total success launches for all sites')
        return fig
    else:
        data_site = spacex_df[spacex_df['Launch Site'] == entered_site]
        data_site = data_site.groupby(['class']).size().reset_index(name='Launch Site')
        fig = px.pie(data_site, values='Launch Site', names='class', title='Total success launches for site ' + entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site, slider_value):
    filtered_spacex_df = spacex_df[spacex_df['Payload Mass (kg)'] >= slider_value[0]]
    filtered_spacex_df = filtered_spacex_df[filtered_spacex_df['Payload Mass (kg)'] <= slider_value[1]]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_spacex_df, x='Payload Mass (kg)', y='class', color="Booster Version Category")
    else:
        data_site = filtered_spacex_df[filtered_spacex_df['Launch Site'] == entered_site]
        
        fig = px.scatter(data_site, x='Payload Mass (kg)', y='class', color="Booster Version Category")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
