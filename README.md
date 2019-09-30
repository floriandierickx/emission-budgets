# emission-budgets
Country-specific emission budgets visualisation. Beta-version accessible on [https://emission-budgets.herokuapp.com/].

# Idea / concept

Idea is to visualise countries remaining carbon budget interactively, based on the [http://www.realclimate.org/index.php/archives/2019/08/how-much-co2-your-country-can-still-emit-in-three-simple-steps/](blogpost) and [www.pik-potsdam.de/~stefan/Country%20CO2%20emissions%202016%20calculator.xlsx](dataset) from Stefan Rahmstorf.

# Data

The original [http://www.realclimate.org/index.php/archives/2019/08/how-much-co2-your-country-can-still-emit-in-three-simple-steps/](dataset) is extended with [https://edgar.jrc.ec.europa.eu/overview.php?v=booklet2018](EDGAR historical emissions from JRC) and [https://databank.worldbank.org/reports.aspx?source=2&series=SP.POP.TOTL&country=#](World Bank Population data). The combined dataset that is used in the application can be found in [https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing](this Google Sheets) (sheet `import`). To be able to display the historical EDGAR emission data for each country, the country order in the original excel sheet has been changed a little bit.

# Working

Note: the app uses Dash and Plotly to create an interactive figure. The script `app.py` is divided in 3 main parts:
1. Data import and definition of global variables : [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L13](link)
2. The app layout with text, interative inputs and outputs : [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L33](link) -> see below for more details
3. A series of 'callback' functions to update the above app layout based on changing inputs : [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L202](link)

Currently, based on a [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L38](given country) and [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L52](carbon budget), the app calculates:

- the [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L256](global reach) of the given carbon budget
- a [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L286](country-specific carbon budget) (2016)
- assuming 2018 and 2019 emissions equal to 2017 emissions (latest data in EDGAR database), it calculates the [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L303](country-specific remaining carbon budget from 2020 onwards), together with years left at [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L314](constant) or [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L326](linearly decreasing) emissions.

# To do / stuck

What would be nice to implement is:

- A function/code/loop that calculates a linear decrease in emissions and feeds this into a series that can be plotted in the third part (`Future` data) in the graph [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L144](here) (static) and [https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L233](here) (dynamic with callback), based on:
  - the country-specific carbon budget left from 2020 onwards : 
  - years left for the country to go to zero :

At the moment it just plots again the historical data

# Workflow

- The app can be run on a local server. See below for more information.
- This github respository is linked to a Heroku application ([https://emission-budgets.herokuapp.com/]), that updates automatically each time the GitHub repository is updated.

## Run the app locally for testing
Note: instructions are for OSX with Homebrew and Anaconda installed.

Information taken from [https://towardsdatascience.com/how-to-create-your-first-web-app-using-python-plotly-dash-and-google-sheets-api-7a2fe3f5d256].

### create conda environment and install required packages
```
conda create --name emission-budgets python=3.6
source activate emission-budgets
pip install dash
pip install dash-renderer
pip install dash-core-components
pip install dash-html-components
pip install plotly
pip install dash-table-experiments
pip install numpy
pip install pandas
pip install gunicorn
pip install google-api-python-clientpip install numpy
pip install pandas
pip install gunicorn
```

### run the app on local server

1. Go to working directory in terminal
2. Activate conda environment with `conda activate emission-budgets`
3. Run the app with `python app.py` (it should display a url with the application that you can open in a browser)
