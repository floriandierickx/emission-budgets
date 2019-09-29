# Google API requirements
from __future__ import print_function
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
import dash
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Pandas Dataframe
import pandas as pd
# import numpy as np

##################################
# Get google carbon budget sheet # CANCELLED AT THE MOMENT, NOT WORRKING IN HEROKU
##################################
# From: https://towardsdatascience.com/how-to-access-google-sheet-data-using-the-python-api-and-convert-to-pandas-dataframe-5ec020564f0e

# # Google API : If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
#
# # Google API : ID and range of spreadsheet.
# SPREADSHEET_ID = '1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo'
# RANGE_NAME = 'import!A1:CC210'
#
# def get_google_sheet(spreadsheet_id, range_name):
#     # Call the Sheets API
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#     service = build('sheets', 'v4', credentials=creds)
#     sheet = service.spreadsheets()
#     result_budget = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
#                                        range=RANGE_NAME).execute()
#     return result_budget
#
# ###########################################################
# # Convert carbon budget sheet to pandas frame 'df_budget' #
# ###########################################################
# # From: https://towardsdatascience.com/how-to-access-google-sheet-data-using-the-python-api-and-convert-to-pandas-dataframe-5ec020564f0e
#
#
# def result2df(result_budget):
#     """ Converts Google sheet data to a Pandas DataFrame.
#     Note: This script assumes that your data contains a header file on the first row!
#     Also note that the Google API returns 'none' from empty cells - in order for the code
#     below to work, you'll need to make sure your sheet doesn't contain empty cells,
#     or update the code to account for such instances.
#     """
#     header = result.get('values', [])[0]   # Assumes first line is header!
#     values = result.get('values', [])[1:]  # Everything else is data.
#     if not values:
#         print('No data found.')
#     else:
#         all_data = []
#         for col_id, col_name in enumerate(header):
#             column_data = []
#             for row in values:
#                 column_data.append(row[col_id])
#             ds = pd.Series(data=column_data, name=col_name)
#             all_data.append(ds)
#         df = pd.concat(all_data, axis=1)
#         return df
#
#
# result = get_google_sheet(SPREADSHEET_ID, RANGE_NAME)
# df_budget = result2df(result)  # name data
# print('Dataframe size = ', df_budget.shape)
# print(df_budget.head())  # print pandas dataframe

###############
# Import data #
###############

df_budget = pd.read_csv("import.csv")

# App interface : https://dash.plot.ly/getting-started
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css']  # select stylesheet
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Country Carbon Budget Calculator'
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Country Carbon Budget Calculator'),  # title of graph
    html.Div([  # start of interactive inputs
        ##################
        # Select country # id : country-dropdown
        ##################
        html.P([  # country selection button
            html.Label('Select your country'),
            # dcc.Input(id='mother_birth', value=1952, type='number'),
            dcc.Dropdown(
                id='country-dropdown',  # name country
                options=[{'label': i, 'value': i} for i in df_budget.country],
                value='Belgium',  # initial value
            )
        ]),
        ########################
        # Select Carbon Budget # id : carbon-budget
        ########################
        html.P([  # country selection button
            html.H3('Carbon Budget'),
            html.P(['Carbon budgets are expressed in Gt CO2, and are used to estimate the amount of carbon dioxide we can still emit before reaching a certain level of warming. For example, to have a 50 % chance to stay below 1.5 °C - *expressed as the 50th percentile of the Transient Climate Response to Cumulative Emissions (TCRC)* - we can emit 580 Gt CO2 calculated from 1 january 2018 onwards. However, some uncertainties remain on this amount. If earth system feedbacks are taken into account, this could decrease with 100 Gt CO2. Other factors not related to CO2 emissions, non-CO2 from other GHGs response uncertainty, distribution of TCRC, historical emission uncertainty and recent emission uncertainty can alter this budget with respectively ±250, -400 to +200, +100 to +200, ±250 and ±20 Gt. Following a precautionary principle, this budget could thus already be depleted. See the ',
            html.A("IPCC's latest report on 1.5 °C warming (Table 2.2)", href='https://hyp.is/LwH2ROKyEem027sdvofrBw/www.ipcc.ch/sr15/chapter/chapter-2/', target='_blank'),
            ' for a range of possible values.'
            ]),
            html.Label('Enter carbon budget in Gt CO2:'),
            # dcc.Input(id='mother_birth', value=1952, type='number'),
            dcc.Input(
                  id='carbon-budget',
                  value=580,
                  type="number",
                  min=50,
                  step=1,
                  max=2500,
            )
        ]),
        #######################
        # Explain calculation #
        #######################
        html.P([
        
        ])
    ]),

    ###########################################
    # CREATE STARTING COUNTRYY BAR GRAPH HERE #
    ###########################################

    dcc.Graph(
        id='emissions-graph',  # Name graph
        # Select first country + Select row based on column value : df.loc[df['favorite_color'] == 'yellow']
        figure={
            'data': [

                # First bar chart with historical values
                go.Bar(
                    name='Historical',
                    x=list(range(1970, 3000)),  # create list from 1970 to 1980
                    y=df_budget.loc[df_budget['country'] == 'Belgium',
                                    '1970':'2017'].values.flatten().tolist(),

                ),

                # Second bar chart with future values

                # go.Bar(
                #     name='Carbon Budget',
                #     # x=list(range(1980,2000)),
                #     y=1,
                # ),

            ],
            'layout': {
                'title': 'Historical Emissions and Future 1.5 Degree Target (linear reduction in emissions)',
            }
        }
    ),
    ###################
    # Background info #
    ###################
    html.H3('Background'),
    html.P(['Created by ', # acknowledgement
            html.A("Florian Dierickx", href='https://floriandierickx.github.io/', target='_blank'),
            ' based on the ',
            html.A("idea", href='http://www.realclimate.org/index.php/archives/2019/08/how-much-co2-your-country-can-still-emit-in-three-simple-steps/', target='_blank'),
            ' and ',
            html.A("data", href='www.pik-potsdam.de/~stefan/Country%20CO2%20emissions%202016%20calculator.xlsx', target='_blank'),
            ' from ',
            html.A("Stefan Rahmstorf", href='https://twitter.com/rahmstorf', target="_blank"),
            ', completemented with ',
            html.A("historical emissions data (EDGAR) from the EU Joint Research Centre", href='https://edgar.jrc.ec.europa.eu/overview.php?v=booklet2018', target="_blank"),
            '.',
    ]),
    html.P(['Find out more about the data on ',
            html.A("Google Sheets", href='https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing', target='_blank'),
            ', get the code, or help improve the application on ',
            html.A("GitHub", href='https://github.com/floriandierickx/emission-budgets', target='_blank'),
            '.',
    ]),
])



# Create callback to update graph with Country selection input (see html.Div) : https://dash.plot.ly/getting-started-part-2

#################################################################
# INSERT CODE TO CREATE BAR PLOT BASED ON SELECTED COUNTRY HERE #
#################################################################


@app.callback(
    Output('emissions-graph', 'figure'),  # insert graph name
    [Input('country-dropdown', 'value')])
def update_figure(selected_country):
    return {
        'data': [go.Bar(
            name='Historical',
            x=list(range(1970, 3000)),  # create list from 1970 to long enough in the future
            y=df_budget.loc[df_budget['country'] == selected_country, '1970':'2017'].values.flatten().tolist(),
        )
        ]
    }


if __name__ == '__main__':
    app.run_server(debug=True)
