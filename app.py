# requirements
from __future__ import print_function
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
import dash
import pandas as pd

###############
# Import data #
###############

df_budget = pd.read_csv("data.csv")

# App interface : https://dash.plot.ly/getting-started
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css']  # select stylesheet
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Carbon Emission Budget Calculator'
server = app.server

# define variables

global_budget_2016 = 580 + 80,
global_emissions = 40,
global_per_capita_emissions = 5.4,

# create app layout

app.layout = html.Div(children=[
    dcc.Markdown(
        dangerously_allow_html=True, children=['''
        # Carbon Emission Budget Calculator
        ## How much CO<sub>2</sub> can your country still emit to stay below **1.5** or **2** °C warming ?
        ''']),
    html.Div([  # start interactive inputs

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

        dcc.Markdown(
            dangerously_allow_html=True, children=['''
            ### A brief introduction to carbon budgets
            Global carbon budgets are expressed in *gigatonnes* (Gt, 1.000.000.000 t) CO<sub>2</sub>,
            and are used to estimate the amount of carbon dioxide we can still emit before reaching
            a certain level of warming.
            For example, for a 50 % chance to stay below **1.5** °C we could still emit around **580** Gt CO<sub>2</sub> from \
            january 2018 onwards. Knowing that we currently emit around  42 ± 3 Gt CO<sub>2</sub> per year,
            this budget already decreased with amost 80 Gt CO<sub>2</sub>. Greta Thunberg thus rightly made this the central \
            issue in her [July speech to the French National Assembly](https://www.youtube.com/watch?v=J1yimNdqhqE).
            However, as with any serious science, some uncertainties remain on this amount. If earth system \
            feedbacks are taken into account, this budget could further decrease with 100 Gt CO<sub>2</sub>. Other factors not \
            related to CO<sub>2</sub> emissions, uncertainties about the temperature response to other greenhouse gasses,
            the distribution of the temperature response to changes in carbon dioxide, \
            historical emissions uncertainty and recent emissions uncertainty can alter this budget with \
            respectively ±250, -400 to +200, +100 to +200, ±250 and ±20 Gt. Following a precautionary \
            principle, a large part of this budget could thus already be depleted. These uncertainties - as [noted by Stefan Rahmstorf](https://hyp.is/ub38EuV2Eem6qrNqE5h7TA/www.realclimate.org/index.php/archives/2019/08/how-much-co2-your-country-can-still-emit-in-three-simple-steps/) \
            - should therefore not be used to argue against strong measures. Only a better guidance providing less uncertainty can improve \
            policy guidance.
            ''']),
            html.P(['See the ',
            html.A("IPCC's latest report on 1.5 °C warming (Table 2.2)",
            href='https://hyp.is/LwH2ROKyEem027sdvofrBw/www.ipcc.ch/sr15/chapter/chapter-2/', target='_blank'),
            ' for a range of possible values which assume the start of the budget in 2018.'
            ]),
        html.P([  # country selection button
            html.Label(['Enter a ',
            html.Span('2018 carbon budget', style={'font-weight': 'bold'}),
            ' in Gt CO2 :']),
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
            html.H3('What is the remaining carbon emission budget for my country?'),
            html.P(['Below figure displays the ',
            html.Span('historical', style={'color': '#1f76b4', 'font-weight': 'bold'}),
            ' and ',
            html.Span('recent', style={'color': '#ff7f0f', 'font-weight': 'bold'}),
            ' emissions in your country, and a linear decrease in ',
            html.Span('future', style={'color': '#2ba02b', 'font-weight': 'bold'}),
            ' emissions from 2020 onwards compatible with the given global carbon budget. The global budget has been divided between countries, \
            starting from the premise that the remaining budget was equally shared per capita in 2016 - the year of the Paris agreement. \
            The emissions in your country in 2018 and 2019 are assumed to have stayed at the same level as in 2017, as this is the latest data available on a global level. \
            The remaining national shares of the global budget from 2019 have been calculated backwards from the given global 2018-budget, by adding 80 Gt to the global budget \
            for two years of emissions since 2016 (2017 and 2018), multiplying with the relative share of the population of your country in the world and substracting two years of emissions \
            in your country since 2016.\
             \
              ']),
        ]),

        ################
        # Global reach #
        ################

        html.P(id='worldwide-reach'),  # create div for variable output with adapted worldwide reach (id: worldwide reach)

        ###############################
        # Country budget and timeline #
        ###############################

        html.P(id='country-carbon-budget'),  # create div for variable output with adapted country carbon budget

    ]),


    #####################
    # Country bar chart #
    #####################

    dcc.Graph(
        id='emissions-graph',  # Name graph
        figure={
            'data': [

                ###################
                # Historical data # : from imported EDGAR dataset
                ###################
                go.Bar(
                    name='Historical',
                    x=list(range(1970, 2018)),  # create list from 1970 to 2017
                    y=df_budget.loc[df_budget['country'] == 'Belgium',       # Select country + Select row based on column value, example : df.loc[df['favorite_color'] == 'yellow']
                                    '1970':'2017'].values.flatten().tolist(),
                ),

                ###############
                # Recent data # : 2018 and 2019 assumed to have same emissions as 2017 (latest EDGAR data available)
                ###############
                go.Bar(
                    name='Recent',
                    x=list(range(2018, 2020)),  # create list from 2018 to 2019
                    y=df_budget.loc[df_budget['country'] == 'Belgium',       # Select country + Select row based on column value, example : df.loc[df['favorite_color'] == 'yellow']
                                    ['2018', '2019']].values.flatten().tolist(),
                ),

                ###############
                # Future data # : compute linear decrease in emissions with given country carbon budget, until zero
                ###############
                go.Bar(
                    name='Future',
                    x=list(range(2020, 3000)),  # create list from 2020 to 3000
                    y=df_budget.loc[df_budget['country'] == 'Belgium',       # Select country + Select row based on column value, example : df.loc[df['favorite_color'] == 'yellow']
                                    '2020':'2100'].values.flatten().tolist(),
                ),
            ],

            'layout': {
                'title': 'Historical Emissions and Future National Emission Budget',
                'xaxis': {
                    'title': 'Year'
                },
                'yaxis': {
                    'title': 'Emissions (Megatons CO2)'
                },

            }
        }
    ),

        html.P([
            html.H3('What does this mean for my personal carbon footprint?'),
            html.P(['Below figure translates your national carbon budget to personal carbon footprints in tonnes CO2.\
             \
              ']),
        ]),


    ######################
    # Personal bar chart #
    ######################

    dcc.Graph(
        id='emissions-graph-personal',  # Name graph
        figure={
            'data': [

                ###############
                # Future data # : compute linear decrease in emissions with given country carbon budget, until zero
                ###############
                go.Bar(
                    name='Future',
                    x=list(range(2020, 3000)),  # create list from 2020 to 3000
                    # y=[((df_budget.loc[df_budget['country'] == 'Belgium',       # Select country + Select row based on column value, example : df.loc[df['favorite_color'] == 'yellow']
                    #                 '2020':'2100'].values.flatten() / (df_budget.loc[df_budget['country'] == 'Belgium', 'population'].values.flatten().tolist()))).tolist())]       # Select country + Select row based on column value, example : df.loc[df['favorite_color'] == 'yellow']

                    y=df_budget.loc[df_budget['country'] == 'Belgium',       # Select country + Select row based on column value, example : df.loc[df['favorite_color'] == 'yellow']
                                    '2020':'2100'].values.flatten().tolist(),


                ),
            ],

            'layout': {
                'title': 'Future Personal Emission Budget',
                'xaxis': {
                    'title': 'Year'
                },
                'yaxis': {
                    'title': 'Emissions (Megatons CO2)'
                },

            }
        }
    ),

    ###################
    # Background info #
    ###################

    html.H3('Credits and Data'),
    html.P(['Created by ',  # acknowledgement
            html.A("Florian Dierickx",
                   href='https://floriandierickx.github.io/', target='_blank'),
            ' based on the ',
            html.A("idea", href='http://www.realclimate.org/index.php/archives/2019/08/how-much-co2-your-country-can-still-emit-in-three-simple-steps/', target='_blank'),
            ' and ',
            html.A("original data", href='www.pik-potsdam.de/~stefan/Country%20CO2%20emissions%202016%20calculator.xlsx', target='_blank'),
            ' from ',
            html.A("Stefan Rahmstorf",
                   href='https://twitter.com/rahmstorf', target="_blank"),
            ', completemented with ',
            html.A("historical carbon emission data (EDGAR) from the EU Joint Research Centre",
                   href='https://edgar.jrc.ec.europa.eu/overview.php?v=booklet2018', target="_blank"),
            ' and ',
            html.A("2016 population data from the World Bank",
                   href='https://databank.worldbank.org/reports.aspx?source=2&series=SP.POP.TOTL&country=#', target="_blank"),
            ]),
    html.P(['Find out more about the data on ',
            html.A("Google Sheets", href='https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing', target='_blank'),
            ', get the code, or help improve the application on ',
            html.A(
                "GitHub", href='https://github.com/floriandierickx/emission-budgets', target='_blank'),
            '.',
            ]),
])

#################################
# UPDATE COUNTRY BAR PLOT BASED #
#################################

@app.callback(
    Output('emissions-graph', 'figure'),   # insert graph name
    [Input(component_id='country-dropdown', component_property='value'),
     Input(component_id='carbon-budget', component_property='value')],)  # country selection

def update_figure(selected_country, carbon_budget):

    # define variables to be used for future emissions

    # emissions in 2019
    emissions_2019 = round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2),

    # time until depletion of budget (round to 0 numbers after the comma)
    t_depletion = (round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2)
                  /
                  ((round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2) ** 2)
                   /
                   (2 * round(((carbon_budget + 80)  # carbon budget country
                              * df_budget.loc[df_budget['country'] == selected_country, 'total_kton_CO2'].values.flatten().tolist()[0])
                              / df_budget.loc[df_budget['country'] == selected_country, 'per_capita_CO2'].values.flatten().tolist()[0]
                              / global_emissions[0]
                              * global_per_capita_emissions[0]
                              / 1000
                              - (2 * df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0]), 2) - round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 0))
                   )
                  ),

    # yearly rate of decrease
    slope = ((round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2) ** 2)
            /
            (2 * round(((carbon_budget + 80)  # carbon budget country
                       * df_budget.loc[df_budget['country'] == selected_country, 'total_kton_CO2'].values.flatten().tolist()[0])
                       / df_budget.loc[df_budget['country'] == selected_country, 'per_capita_CO2'].values.flatten().tolist()[0]
                       / global_emissions[0]
                       * global_per_capita_emissions[0]
                       / 1000
                       - (2 * df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0]), 2) - round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 0))),


    # for loop to create list with decreasing emission values
    t_depletion_int = int(t_depletion[0]) # create integer value of year to go to zero (remove numbers after the comma: transform from float to int)
    future = [] # create empty list
    for t in range(1, t_depletion_int): # fill list with decreasing emission values
        future.append(round(emissions_2019[0], 2) - round(slope[0], 2) * t)

    # update figures
    return {
        'data': [go.Bar(

            ###################
            # Historical data # : from imported EDGAR dataset
            ###################
            name='Historical',
            x=list(range(1970, 2018)),
            y=df_budget.loc[df_budget['country'] == selected_country,  # Select country + Select row based on column value,
                                                                       # example : df.loc[df['favorite_color'] == 'yellow']
                            '1970':'2017'].values.flatten().tolist(),
        ),

            ###############
            # Recent data # : 2018 and 2019 assumed to have same emissions as 2017 (latest EDGAR data available)
            ###############
            go.Bar(
            name='Recent',
            x=list(range(2018, 2020)),
            y=df_budget.loc[df_budget['country'] == selected_country,
                            '2018':'2019'].values.flatten().tolist(),
        ),

            ###############
            # Future data # : compute linear decrease in emissions with given country carbon budget until zero
            ############### with function describing emission value for years from 2020
            go.Bar(
            name='Future',
            x=list(range(2020, 3000)),
            y=future,
        ),
        ],
        'layout': {
            'title': 'Historical Emissions and Future Emission Budget for {}'.format(selected_country),
            'xaxis': {
                'title': 'Year'
            },
            'yaxis': {
                'title': 'National Emissions (Megatons CO2)'
            },
        },
    }

############################
# UPDATE PERSONAL BAR PLOT #
############################

@app.callback(
    Output('emissions-graph-personal', 'figure'),   # insert graph name
    [Input(component_id='country-dropdown', component_property='value'),
     Input(component_id='carbon-budget', component_property='value')],)  # country selection

def update_figure(selected_country, carbon_budget):

    # define variables to be used for future emissions

    # emissions in 2019
    emissions_2019 = round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2),

    # time until depletion of budget (round to 0 numbers after the comma)
    t_depletion = (round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2)
                  /
                  ((round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2) ** 2)
                   /
                   (2 * round(((carbon_budget + 80)  # carbon budget country
                              * df_budget.loc[df_budget['country'] == selected_country, 'total_kton_CO2'].values.flatten().tolist()[0])
                              / df_budget.loc[df_budget['country'] == selected_country, 'per_capita_CO2'].values.flatten().tolist()[0]
                              / global_emissions[0]
                              * global_per_capita_emissions[0]
                              / 1000
                              - (2 * df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0]), 2) - round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 0))
                   )
                  ),

    # yearly rate of decrease
    slope = ((round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2) ** 2)
            /
            (2 * round(((carbon_budget + 80)  # carbon budget country
                       * df_budget.loc[df_budget['country'] == selected_country, 'total_kton_CO2'].values.flatten().tolist()[0])
                       / df_budget.loc[df_budget['country'] == selected_country, 'per_capita_CO2'].values.flatten().tolist()[0]
                       / global_emissions[0]
                       * global_per_capita_emissions[0]
                       / 1000
                       - (2 * df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0]), 2) - round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 0))),

    # country population
    population = round(df_budget.loc[df_budget['country'] == selected_country, 'population'].values.flatten().tolist()[0], 2),



    # for loop to create list with decreasing emission values
    t_depletion_int = int(t_depletion[0]) # create integer value of year to go to zero (remove numbers after the comma: transform from float to int)
    future = [] # create empty list
    for t in range(1, t_depletion_int): # fill list with decreasing emission values
        future.append((1000000 * (round(emissions_2019[0], 2) / round(population[0], 2))) - (1000000 * ((round(slope[0], 2) / round(population[0], 2)) * t)))

    # update figures
    return {
        'data': [

            ###############
            # Recent data #
            ###############

        #     go.Bar(
        #     name='Recent',
        #     x=list(range(2018, 2020)),
        #     y=df_budget.loc[df_budget['country'] == selected_country,
        #                     '2018':'2019'].values.flatten().tolist(),
        # ),

            go.Bar(
            name='Recent',
            marker_color='rgb(255,127,15)',
            x=list(range(2019, 2020)),
            y=(1000000 * (df_budget.loc[df_budget['country'] == selected_country,
                            '2018'].values.flatten() / (round(population[0], 2)))).tolist(),
        ),

            ###############
            # Future data # : compute linear decrease in emissions with given country carbon budget until zero
            ############### with function describing emission value for years from 2020
            go.Bar(
            name='Future',
            marker_color='rgb(106,187,104)',
            x=list(range(2020, 3000)),
            # y=future_personal,
            y = future,
        ),

        ],
        'layout': {
            'title': 'Personal Future Emission Budget in {}'.format(selected_country),
            'xaxis': {
                'title': 'Year'
            },
            'yaxis': {
                'title': 'Personal Emissions (tons CO2)'
            },
        },
    }


############################
# CALCULATE COUNTRY BUDGET # : id : country-carbon-budget
############################


@app.callback(
    Output(component_id='country-carbon-budget',
           component_property='children'),
    [Input(component_id='country-dropdown', component_property='value'),
     Input(component_id='carbon-budget', component_property='value')]
)

def update_country_div(selected_country, carbon_budget):
    style = {'font-weight': 'bold'}
    return ['In 2016, it would have taken ',
    html.Span('{}'.format((carbon_budget + 80) / 40,), style=style), # Global reach from 2016 onwards
    ' years of constant worldwide emissions before the carbon budget was depleted. \
    From 2020 onwards, this will be reduced to ',
    html.Span('{}'.format(((carbon_budget + 80) / 40) - 4,), style=style), # Global reach from 2020 onwards
    ' years. In 2016, the remaining carbon budget for your country was ',
    html.Span('{}'.format(round(((carbon_budget + 80)  # country carbon budget from 2016 onwards
                               * df_budget.loc[df_budget['country'] == selected_country, 'total_kton_CO2'].values.flatten().tolist()[0])
                              / df_budget.loc[df_budget['country'] == selected_country, 'per_capita_CO2'].values.flatten().tolist()[0]
                              / global_emissions[0]
                              * global_per_capita_emissions[0]
                              / 1000, 2),), style=style),
    ' Mton CO2. \
    Assuming that the 2018 and 2019-emissions in your country stayed at the level of ',
    html.Span('{}'.format(round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2),), style=style), # country emissions 2017
    ' Mton CO2 in 2017, the remaining national carbon\
    budget from 2020 onwards is ',
    html.Span('{}'.format(round(((carbon_budget + 80)  # carbon budget country
                              * df_budget.loc[df_budget['country'] == selected_country, 'total_kton_CO2'].values.flatten().tolist()[0])
                              / df_budget.loc[df_budget['country'] == selected_country, 'per_capita_CO2'].values.flatten().tolist()[0]
                              / global_emissions[0]
                              * global_per_capita_emissions[0]
                              / 1000 - (2 * df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0]), 2),), style=style), # country carbon budget from 2019 onwards
    ' Mton CO2. This is equal to ',
    html.Span('{}'.format(round((((carbon_budget + 80)  # carbon budget country
          * df_budget.loc[df_budget['country'] == selected_country, 'total_kton_CO2'].values.flatten().tolist()[0])
          / df_budget.loc[df_budget['country'] == selected_country, 'per_capita_CO2'].values.flatten().tolist()[0]
          / global_emissions[0]
          * global_per_capita_emissions[0]
          / 1000 - (2 * df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0]))
          / df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2),), style=style), # years in cte emissions from 2019 onwards
    ' years of constant emissions, or ',
    html.Span('{}'.format(round((round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2)
     /
     ((round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2) ** 2)
        /
        (2 * round(((carbon_budget + 80)  # carbon budget country
                    * df_budget.loc[df_budget['country'] == selected_country, 'total_kton_CO2'].values.flatten().tolist()[0])
                   / df_budget.loc[df_budget['country'] == selected_country, 'per_capita_CO2'].values.flatten().tolist()[0]
                   / global_emissions[0]
                   * global_per_capita_emissions[0]
                   / 1000 - (2 * df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0]), 2)
                   - round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2))
     )
    ), 2),), style=style), # Global reach from 2016 onwards
    ' years when linearly decreasing emissions.']

if __name__ == '__main__':
    app.run_server(debug=True)
