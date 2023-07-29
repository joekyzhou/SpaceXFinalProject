# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

#Create the list of options for the dropdown
launch_site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                            id='site-dropdown',
                                            options=launch_site_options,
                                            value='ALL',
                                        ),
                                
                                html.Br(), #creates a break line or new line

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                                id='payload-slider',
                                                min=int(min_payload),
                                                max=int(max_payload),
                                                value=[int(min_payload), int(max_payload)],
                                                marks={payload: str(payload) for payload in range(int(min_payload), int(max_payload) + 1, 1000)},
                                            ),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                            ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site' )
        return fig
    else:
        # Count the successful and failed launches for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        pie_data = filtered_df['class'].value_counts()

    # Create and return the pie chart figure
        fig = px.pie(pie_data, names=pie_data.index, values=pie_data.values, title="Total Success vs Failure Launches for site " + entered_site )
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter data based on selected site and payload range
    if selected_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        filtered_df = site_df[(site_df['Payload Mass (kg)'] >= payload_range[0]) &
                              (site_df['Payload Mass (kg)'] <= payload_range[1])]

    # Create and return the scatter chart figure
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True) #debug=True will help us update the dashboard as we are editing here for debugs
