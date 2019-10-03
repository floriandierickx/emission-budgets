[![DOI](https://zenodo.org/badge/211486285.svg)](https://zenodo.org/badge/latestdoi/211486285)

# Concept

Visualising national and personal remaining carbon budgets interactively, based on the [blogpost](http://www.realclimate.org/index.php/archives/2019/08/how-much-co2-your-country-can-still-emit-in-three-simple-steps/) and [dataset](www.pik-potsdam.de/~stefan/Country%20CO2%20emissions%202016%20calculator.xlsx) from Stefan Rahmstorf. This could be further extended with different types of carbon budget calculation.

# Data sources

The original [dataset](http://www.realclimate.org/index.php/archives/2019/08/how-much-co2-your-country-can-still-emit-in-three-simple-steps/) is extended with [EDGAR historical emissions data from JRC](https://edgar.jrc.ec.europa.eu/overview.php?v=booklet2018) and [World Bank Population data](https://databank.worldbank.org/reports.aspx?source=2&series=SP.POP.TOTL&country=#). The combined dataset that is used in the application can be found in [this google sheet](https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing) (imported sheet = `import`). To be able to display the historical EDGAR emission data for each country, the country order in the original excel sheet has been changed a little bit.

# Structure of the code

Note: the app uses Dash and Plotly to create an interactive figure. The script `app.py` is divided in 3 main parts:

1. Data import and definition of global variables : [code link](https://github.com/floriandierickx/emission-budgets/blob/1f2e65f56a09f20433d356fd3ebe405c877f1ada/app.py#L11)
   - `df_budget = pd.read_csv("data.csv")` : importing the `data.csv` file, which is the same as the `input` sheet in the [google sheets](https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing)
   - definition of global variables:
      - `global_budget_2016 = 580 + 80` : used for testing, not reused in the code
      - `global_emissions = 40` : global emissions in 2016 (Gt CO2), taken from the [google sheets](https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing), cell `E16`
      - `global_per_capita_emissions = 5.4` : global per capita emissions in 2016 (t CO2), taken from the [google sheets](https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing), cell `E18`
2. The app layout with text, interative inputs and outputs : [code link](https://github.com/floriandierickx/emission-budgets/blob/1f2e65f56a09f20433d356fd3ebe405c877f1ada/app.py#L31). It contains
   - A **country-selection box**, id = `country-dropdown` to be selected from `df_budget.country`
   - **Global carbon budget input**, id = `carbon-budget` to stay within the range of `50` and `2500`
   - **Global reach of global carbon budget paragraph** :, id = `global-reach`
   - **Country carbon budget and timeline**, id = `country-carbon-budget`
   - a **bar chart** (id: `emission-graph`) displaying:
     - ***Historical emissions*** : [code link](https://github.com/floriandierickx/emission-budgets/blob/1f2e65f56a09f20433d356fd3ebe405c877f1ada/app.py#L144)
     - ***"Recent" (2018/2019) emissions*** : [code link](https://github.com/floriandierickx/emission-budgets/blob/1f2e65f56a09f20433d356fd3ebe405c877f1ada/app.py#L154)
     - ***Future linear decrease in country carbon budget*** : [code link](https://github.com/floriandierickx/emission-budgets/blob/1f2e65f56a09f20433d356fd3ebe405c877f1ada/app.py#L164)
   - **Personal carbon emissions projection** : [code link](https://github.com/floriandierickx/emission-budgets/blob/1f2e65f56a09f20433d356fd3ebe405c877f1ada/app.py#L196)
   - **Credits and data** : [code link](https://github.com/floriandierickx/emission-budgets/blob/1f2e65f56a09f20433d356fd3ebe405c877f1ada/app.py#L234)
3. A series of 'callback' functions to update the above app layout based on changing inputs, [code link](https://github.com/floriandierickx/emission-budgets/blob/4578f0b1fd0ade04d289d75fef4621d751529e51/app.py#L202) :
   - **Update of the country emission graph** (id: `emission-graph`) based on country : [code link](https://github.com/floriandierickx/emission-budgets/blob/1f2e65f56a09f20433d356fd3ebe405c877f1ada/app.py#L268)
   - **Update of the personal emission graph** (id: `emission-graph`) based on country : [code link](https://github.com/floriandierickx/emission-budgets/blob/1f2e65f56a09f20433d356fd3ebe405c877f1ada/app.py#L358)
   - Calculation of the **global reach of the given global emission budget**, **country-specific budgets**, **country-specific carbon budget (2016)**, **country-specific carbon budget from 2019 onwards**, **years left at constant emissions** or **linearly decreasing emissions** [code link](https://github.com/floriandierickx/emission-budgets/blob/1f2e65f56a09f20433d356fd3ebe405c877f1ada/app.py#L458)

# Detailed information on calculations

- The **country-specific annual emission in 2017, 2018 or 2019**: assumed to have stayed the same as in 2017, as is this the latest data available for all the countries in the JRC EDGAR historical emission database (and 2019 is almost over). This yearly emission data for a specific country can be taken directly from the imported dataset using
  ```python
  round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2),
  ```
  (see [line 299](https://github.com/floriandierickx/emission-budgets/blob/21ef1b909c20e65c9a22da714e19d46104c9270f/app.py#L299))

- The **country-specific emission budget that can be used from 2016 onwards** (year of the Paris agreement). This value can be calculated from the data using (see [lines 288 to 293](https://github.com/floriandierickx/emission-budgets/blob/21ef1b909c20e65c9a22da714e19d46104c9270f/app.py#L288), based on the premise that the budget is distributed on an equal per capita basis at the start of 2016.
  ```python
  round(((carbon_budget + 80)  # carbon budget country
      * df_budget.loc[df_budget['country'] == selected_country,   'total_kton_CO2'].values.flatten().tolist()[0])
      / df_budget.loc[df_budget['country'] == selected_country,   'per_capita_CO2'].values.flatten().tolist()[0]
      / global_emissions[0]
      * global_per_capita_emissions[0]
      / 1000, 2),
  ```
  This value is calculated as:
  <img width="896" alt="Screenshot 2019-09-30 at 17 53 58" src="https://user-images.githubusercontent.com/12695083/65895165-4c44c980-e3ab-11e9-85b4-fb5fd99cc875.png">

  (taken from the [spreadsheet](https://docs.google.com/spreadsheets/d/1R1U8iwlf2NdHDj6ykzgUqocQDfpbVB6i8lsStN3eNlo/edit?usp=sharing) of Stefan Rahmstorf - for example cell E25 for Afghanistan in the `original` sheet. I hope I interpreted it here correctly)

- The **country-specific emission budget that is left to deplete from 2019 onwards**, accounting for the 2 years that have already passed: this can be calculated by using the above 2016-country emission budget and deducing two years of constant 2017-emissions (see [lines 305-310](https://github.com/floriandierickx/emission-budgets/blob/472c6792fa246b28cca8886138d673409e73a518/app.py#L305)), by substracting
  ```python
  - (2 * df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0]), 2)
  ```

- From then it is straightforward to calculate the **remaining years left at constant emissions** for each country, by dividing the remaining carbon budget from 2019 onwards by a constant 2017 (or 2018/2019) emission level, as done in [line 316 to 322](https://github.com/floriandierickx/emission-budgets/blob/472c6792fa246b28cca8886138d673409e73a518/app.py#L316).

  ```python
  / df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2)
  ```

- To calculate the **time before depletion** and **yearly rate of emission decrease** in the case of linear decrease until the remaining budget is depleted [emissions(t) = emissions(2019) - slope . t(depletion)] we can start from the premise that the total budget (`budget`) and starting emissions (`emissions_2019`) are known, out of which we can calculate the `slope` (rate of decrease) and time before depletion (`t_depletion`):

  *System of equations*:

  ![](https://i.imgur.com/B28904u.png)

  *Solution*:

  ![](https://i.imgur.com/OL6TRsj.png)

  - As emissions in 2019 are assumed to be fixed, the remaining budget before linear decrease needs to be reduced with the 2019 emissions. The depletion time can be then be calculated as:

    ```python
    (round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2)
             /
             ((round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2) ^ 2)
                /
                (2 * round(((carbon_budget + 80)  # carbon budget country
                            * df_budget.loc[df_budget['country'] == selected_country, 'total_kton_CO2'].values.flatten().tolist()[0])
                           / df_budget.loc[df_budget['country'] == selected_country, 'per_capita_CO2'].values.flatten().tolist()[0]
                           / global_emissions[0]
                           * global_per_capita_emissions[0]
                           / 1000
                           - (2 * df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0]), 2) - round(df_budget.loc[df_budget['country'] == selected_country, '2017'].values.flatten().tolist()[0], 2))
             )
            )
    ```

# Development and workflow

- The app can be run on a local server. See below for more information.
- This github respository is linked to a Heroku application (https://emission-budgets.herokuapp.com/), that updates automatically each time the GitHub repository is updated.

## Running the app locally for testing
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

### Running the app on a local host

1. Go to working directory in terminal
2. Activate conda environment with `conda activate emission-budgets`
3. Run the app with `python app.py` (it should display a url with the application that you can open in a browser)
