# emission-budgets
Country-specific emission budgets visualisation

# idea

Idea is to visualise blogpost [http://www.realclimate.org/index.php/archives/2019/08/how-much-co2-your-country-can-still-emit-in-three-simple-steps/] and dataset [www.pik-potsdam.de/~stefan/Country%20CO2%20emissions%202016%20calculator.xlsx] from Stefan Rahmstorf

# procedure : run locally

Note: below instructions are for OSX with Homebrew installed.

Taken from [https://towardsdatascience.com/how-to-create-your-first-web-app-using-python-plotly-dash-and-google-sheets-api-7a2fe3f5d256]

## create conda enviroment and install required packages
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

## generate project dependencies file

In project folder (terminal): `pip freeze > requirements.txt`

## Install Heroku if not yet done

`brew tap heroku/brew && brew install heroku`

## Create Heroku app

```
heroku create lava-vino # replace "lava-vino" with your-app-name
git add .
git commit -m "Initial commit"
git push heroku master
heroku ps:scale web=1
```

### If this fails: adjust build packs
Background: [https://stackoverflow.com/questions/41804507/h14-error-in-heroku-no-web-processes-running] and [https://help.heroku.com/W23OAFGK/why-am-i-seeing-couldn-t-find-that-process-type-when-trying-to-scale-dynos]
```
heroku buildpacks:clear
heroku buildpacks:add --index heroku/python
git commit --allow-empty -m "Adjust buildpacks on Heroku"
git push heroku master
```

## Update Heroku app
