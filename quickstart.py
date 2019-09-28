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
import numpy as np


# Google API : If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Google API : ID and range of spreadsheet.
SPREADSHEET_ID = '1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo'
RANGE_NAME = 'import!A1:CC210'

# Google API : Example code (from https://developers.google.com/sheets/api/quickstart/python)

# def main():
#     """Shows basic usage of the Sheets API.
#     Prints values from a sample spreadsheet.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
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
#
#     service = build('sheets', 'v4', credentials=creds)
#
#     # Call the Sheets API
#     sheet = service.spreadsheets()
#     result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
#                                 range=RANGE_NAME).execute()
#     values = result.get('values', [])
#
#     if not values:
#         print('No data found.')
#     else:
#         print('Name, Major:')
#         for row in values:
#             # Print columns A and E, which correspond to indices 0 and 4.
#             print('%s, %s' % (row[0], row[4]))
#
# # if __name__ == '__main__':
# #     main()

##################################
# Get google carbon budget sheet #
##################################

# From: https://towardsdatascience.com/how-to-access-google-sheet-data-using-the-python-api-and-convert-to-pandas-dataframe-5ec020564f0e


def get_google_sheet(spreadsheet_id, range_name):
    # Call the Sheets API
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result_budget = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                       range=RANGE_NAME).execute()
    return result_budget

###########################################################
# Convert carbon budget sheet to pandas frame 'df_budget' #
###########################################################

# From: https://towardsdatascience.com/how-to-access-google-sheet-data-using-the-python-api-and-convert-to-pandas-dataframe-5ec020564f0e


def result2df(result_budget):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.
    """
    header = result.get('values', [])[0]   # Assumes first line is header!
    values = result.get('values', [])[1:]  # Everything else is data.
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df


result = get_google_sheet(SPREADSHEET_ID, RANGE_NAME)
df_budget = result2df(result)  # name data
print('Dataframe size = ', df_budget.shape)
print(df_budget.head())  # print pandas dataframe


# App interface : https://dash.plot.ly/getting-started
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css']  # select stylesheet
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Country Carbon Budget Calculator'
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Country Carbon Budget Calculator'),  # title of graph

    html.Div([  # start of interactive inputs

        ###############################
        # Select country in dashboard #
        ###############################

        html.P([  # country selection button
            html.Label('Select your country'),
            # dcc.Input(id='mother_birth', value=1952, type='number'),
            dcc.Dropdown(
                id='country-dropdown',  # name country
                options=[{'label': i, 'value': i} for i in df_budget.country],
                value='Belgium',
            )
        ])]),  # stop interactive inputs

    ###########################################
    # CREATE STARTING COUNTRYY BAR GRAPH HERE #
    ###########################################

    dcc.Graph(
        id='emissions-graph',  # Name graph
        # Select first country + Select row based on column value : df.loc[df['favorite_color'] == 'yellow']
        # df_budget_country_transposed = df_budget_country.transpose()
        figure={
            'data': [

                # First bar chart with historical values

                go.Bar(
                    name='Historical',

                    x=list(range(1970, 1980)), # create list from 1970 to 1980


                    y=list(np.float_(df_budget.loc[df_budget['country'] == 'Belgium', '1970':'1979'].values.tolist())),


                    #DEMO (working)
                    #x=[20.1, 14, 23.4], # example
                    #y=['giraffes', 'orangutans', 'monkeys'],

                    #TRYOUTS
                    # x=df_budget_country.loc[:,'1970':'1980'],
                    # df_budget_country=df_budget[df_budget['country'] == 'Belgium'], # select values for given range of years based on label (column) [or index (row) ]) : .loc[row-range,column-range]
                    #y=df_budget.loc[:, '1970':'1980'],
                    #y=df_budget.loc[df_budget['country'] == 'Belgium', '1970':'1980'].transpose().values.tolist(), # select total emissions from Belgium from 1970 to 1980
                    # y=df_budget.loc[df_budget['country'] == 'Belgium', '1970':'1980'].values.tolist(),

                ),

                # Second bar chart with future values

                # go.Bar(
                #     name = 'Future',
                #     x=list(range(1980,2000)),
                #
                # ),

                # {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                # {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Historical Emissions and Future 1.5 Degree Target (linear reduction in emissions)',
            }
        }
    )
])

# Create callback to update graph with Country selection input (see html.Div) : https://dash.plot.ly/getting-started-part-2

#################################################################
# INSERT CODE TO CREATE BAR PLOT BASED ON SELECTED COUNTRY HERE #
#################################################################

# Start code :

# @app.callback(
#     Output('emissions-graph', 'figure'),  # insert graph name
#     [Input('country-dropdown', 'value')])
# def update_figure(selected_country):
#     # filter country-list with selected country
#     filtered_df_budget = df_budget[df_budget.country == selected_country]
#     traces = []
#     for i in filtered_df_budget.country.unique():
#         df_budget_by_country = filtered_df_budget[filtered_df_budget['country'] == i]
#         traces.append(go.Bar(
#
# # OLD:
#             # x=df_budget_by_country['gdpPercap'],
#             # y=df_budget_by_country['lifeExp'],
#             # text=df_budget_by_country'country'],
#             # mode='markers',
#             # opacity=0.7,
#             # marker={
#             #     'size': 15,
#             #     'line': {'width': 0.5, 'color': 'white'}
#             # },
#             # name=i
#
# # END OLD
#
#         ))

# End code


if __name__ == '__main__':
    app.run_server(debug=True)
