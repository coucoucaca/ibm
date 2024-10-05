# Import required libraries
import pandas as pd
import dash
from dash import dcc, html  
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()




# app = Dash()
# Initialize the Dash app
app = dash.Dash(__name__)

# Create a dash application
# app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, 
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}, 
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, 
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}, 
                                            
                                                ],
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
                                dcc.RangeSlider(
                                            id='payload-slider',
                                            min=0, 
                                            max=10000, 
                                            step=1000,
                                            
                                            marks={0: '0',
                                                2500: '2500',5000: '5000',7500: '7500'},
                                            value=[min_payload, max_payload]) ,

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
              )

def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        fig = px.pie(spacex_df, 
        values='class', 
        names ='Launch Site',
        title=entered_site
        )
        return fig
    else:
        spacex_df2=spacex_df[['Launch Site' , 'class']]
        df3= spacex_df2[spacex_df['Launch Site']== entered_site]
        filtered_df=df3.groupby(['class']).value_counts().reset_index()
       
   
    # return the outcomes piechart for a selected site
        fig = px.pie(filtered_df, 
        values='count', 
        names ='class',
        title= 'Success launches for site ' + entered_site
        )
        return fig

# def update_output(value):
#     return 'You have selected "{}"'.format(value)
        

# max_payload = spacex_df['Payload Mass (kg)'].max()
# min_payload = spacex_df['Payload Mass (kg)'].min()

        

 
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")
              ]
              )
# 'Payload Mass (Kg)'
def get_success_payload_scatter_chart(entered_site, payload_slider ):
    # filtered_df=spacex_df[(spacex_df['Payload Mass (Kg)'] >= payload_slider[0]) & (spacex_df['Payload Mass (kg)']<= payload_slider[1])]
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=payload_slider[0]) &(spacex_df['Payload Mass (kg)']<=payload_slider[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', 
        y='class', 
        color='Booster Version Category',
        title='Correlation between Success rate and Paylod Mass for all sites')
        return fig
    else:
         # return the outcomes for  selected site

        spacex_df_payload=filtered_df[['Launch Site' , 'class', 'Payload Mass (kg)','Booster Version Category']]
        spacex_df_payload_2= spacex_df_payload[spacex_df_payload['Launch Site']== entered_site]
        
        fig = px.scatter(spacex_df_payload_2, 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category',
            title='Correlation between Success rate and Paylod Mass for ' + entered_site)
        return fig


# Run the app
# if __name__ == '__main__':
#     app.run_server()

# if __name__ == '__main__':
#     app.run_server(debug=True)
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)  
