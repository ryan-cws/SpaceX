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

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id = 'site-dropdown',
                                    options = [
                                        {'label':'All sites','value':'All sites'},
                                        {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                        {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                        {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                        {'label': 'CCAFS LC-40','value': 'CCAFS LC-40'}
                                    ],
                                    value = 'All sites',
                                    placeholder = 'Select a Launch Site',
                                    searchable = True
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
                                                value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown',component_property='value')
)

def update_pie_chart (selected_site):
    if selected_site == 'All sites':
        filtered_df = spacex_df
        fig = px.pie(filtered_df, values = 'class', names = 'Launch Site', title = 'Total Successful Launches By Sites' )
    elif selected_site == 'CCAFS SLC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        fig = px.pie(filtered_df, values = 'Flight Number', names = 'class', title = 'Total Successful Launches at CCAFS SLC-40' )
    elif selected_site == 'CCAFS LC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        fig = px.pie(filtered_df, values = 'Flight Number', names = 'class', title = 'Total Successful Launches at CCAFS LC-40' )
    elif selected_site == 'KSC LC-39A':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        fig = px.pie(filtered_df, values = 'Flight Number', names = 'class', title = 'Total Successful Launches at KSC LC-39A' )
    elif selected_site == 'VAFB SLC-4E':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        fig = px.pie(filtered_df, values = 'Flight Number', names = 'class', title = 'Total Successful Launches at VAFB SLC-4E' )
    return fig

    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),Input(component_id='payload-slider',component_property='value')]
    # Input(component_id='site-dropdown',component_property='value')
)

def update_scatter_chart(selected_site,value):
    if selected_site == 'All sites':
        filtered_df = spacex_df
        fig = px.scatter(filtered_df,x='Payload Mass (kg)',y='class',title='Correlation between Payload Mass and Success Rate for All Sites', color='Booster Version Category')
    elif selected_site == 'CCAFS SLC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        fig = px.scatter(filtered_df,x='Payload Mass (kg)',y='class',title='Correlation between Payload Mass and Success Rate for CCAFS SLC-40',color='Booster Version Category')
    elif selected_site == 'CCAFS LC-40':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        fig = px.scatter(filtered_df,x='Payload Mass (kg)',y='class',title='Correlation between Payload Mass and Success Rate for CCAFS LC-40',color='Booster Version Category')
    elif selected_site == 'KSC LC-39A':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        fig = px.scatter(filtered_df,x='Payload Mass (kg)',y='class',title='Correlation between Payload Mass and Success Rate for KSC LC-39A',color='Booster Version Category')
    elif selected_site == 'VAFB SLC-4E':
        filtered_df = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        fig = px.scatter(filtered_df,x='Payload Mass (kg)',y='class',title='Correlation between Payload Mass and Success Rate for VAFB SLC-4E',color='Booster Version Category')
    fig.update_layout(xaxis_range=value)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
