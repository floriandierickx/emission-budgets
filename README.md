# emission-budgets
Country-specific emission budgets visualisation. Beta-version accessible on https://emission-budgets.herokuapp.com/.

# Idea / concept

Idea is to visualise countries remaining carbon budget interactively, based on the [blogpost](http://www.realclimate.org/index.php/archives/2019/08/how-much-co2-your-country-can-still-emit-in-three-simple-steps/) and [dataset](www.pik-potsdam.de/~stefan/Country%20CO2%20emissions%202016%20calculator.xlsx) from Stefan Rahmstorf.

# Data sources

The original [dataset](http://www.realclimate.org/index.php/archives/2019/08/how-much-co2-your-country-can-still-emit-in-three-simple-steps/) is extended with [EDGAR historical emissions data from JRC](https://edgar.jrc.ec.europa.eu/overview.php?v=booklet2018) and [World Bank Population data](https://databank.worldbank.org/reports.aspx?source=2&series=SP.POP.TOTL&country=#). The combined dataset that is used in the application can be found in [this google sheet](https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing) (imported sheet = `import`). To be able to display the historical EDGAR emission data for each country, the country order in the original excel sheet has been changed a little bit.

# What is currently working

Note: the app uses Dash and Plotly to create an interactive figure. The script `app.py` is divided in 3 main parts:
1. Data import and definition of global variables : [code link](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L13)
   - `df_budget = pd.read_csv("data.csv")` : importing the `data.csv` file, which is the same as the `input` sheet in the [google sheets](https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing)
   - definition of global variables:
      - `global_budget_2016 = 580 + 80` : used for testing, not reused in the code
      - `global_emissions = 40` : global emissions in 2016 (Gt CO2), taken from the [google sheets](https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing), cell `E16`
      - `global_per_capita_emissions = 5.4` : global per capita emissions in 2016 (t CO2), taken from the [google sheets](https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing), cell `E18`
2. The app layout with text, interative inputs and outputs : [code link](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L33). It contains
   - A **country-selection box**, id = `country-dropdown` to be selected from `df_budget.country`
   - **Global carbon budget input**, id = `carbon-budget` to stay within the range of `50` and `2500`
   - **Global reach of global carbon budget paragraph** :, id = `global-reach`. This gets filled in later based on the inputs in an `@app.callback` part : [code link](https://github.com/floriandierickx/emission-budgets/blob/472c6792fa246b28cca8886138d673409e73a518/app.py#L259)
   - **Country carbon budget and timeline**, id = `country-carbon-budget`. Gets filled in based on `@app.callback` : [code link](https://github.com/floriandierickx/emission-budgets/blob/472c6792fa246b28cca8886138d673409e73a518/app.py#L267)
   - a **bar chart** (id: `emission-graph`) displaying:
     - ***Historical emissions*** : [code link](https://github.com/floriandierickx/emission-budgets/blob/51e338669ddeb379829c949c790ac6ebafc68bfe/app.py#L123)
     - ***"Recent" (2018/2019) emissions*** : [code link](https://github.com/floriandierickx/emission-budgets/blob/51e338669ddeb379829c949c790ac6ebafc68bfe/app.py#L133)
     - *TO DO* : implement ***future linear decrease in country carbon budget*** : [code link](https://github.com/floriandierickx/emission-budgets/blob/51e338669ddeb379829c949c790ac6ebafc68bfe/app.py#L143)
3. A series of 'callback' functions to update the above app layout based on changing inputs, [code link](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L202) :
   - **Update of the emission graph** (id: `emission-graph`) based on country : [code link](https://github.com/floriandierickx/emission-budgets/blob/51e338669ddeb379829c949c790ac6ebafc68bfe/app.py#L204)
   - Calculation of the **global reach of the given global emission budget** [code link](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L256)
   - Calculation of a **country-specific carbon budgets**, divided in:
     - ***Country-specific carbon budget in 2016*** (year of the Paris agreement) : [code link](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L286)
     - ***Country-specific carbon budget remaining from 2019 onwards*** : [code link](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L303)
   - Calculation of country-specific years left at [constant (code link)](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L314) or [linearly decreasing !this might not be correct! (code link)](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L326) emissions.

# To do / stuck:

What would be nice to implement is:

- A function/code/loop that calculates a linear decrease in emissions and feeds this into a series that can be plotted in the third part (`Future` data) in the graph [here (code link)](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L144) (static) and [here (code link)](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L233) (dynamic with callback), based on:
  - the country-specific carbon budget left from 2020 onwards : [code link](https://github.com/floriandierickx/emission-budgets/blob/ffbcb24ce65d473483d3ebdcf492fc135316b984/app.py#L303)
  - years left for the country to go to zero : [code link](https://github.com/floriandierickx/emission-budgets/blob/ffbcb24ce65d473483d3ebdcf492fc135316b984/app.py#L326)

At the moment it just plots again the historical data.

Help is welcome!

UPDATE : more detailed information on how this could be calculated is discussed in [https://github.com/floriandierickx/emission-budgets/issues/1](this issue).

# Workflow

- The app can be run on a local server. See below for more information.
- This github respository is linked to a Heroku application (https://emission-budgets.herokuapp.com/), that updates automatically each time the GitHub repository is updated.

## Run the app locally for testing
Note: instructions are for OSX with Homebrew and Anaconda installed.

Information taken from https://towardsdatascience.com/how-to-create-your-first-web-app-using-python-plotly-dash-and-google-sheets-api-7a2fe3f5d256.

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
