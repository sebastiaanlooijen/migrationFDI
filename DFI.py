# This scripts cleans and merges all the files in ./Sources
# Sebastiaan Looijen, february 2021

# Import libraries --------------------------------------------------------
import pandas as pd

# Read files from ./Sources -----------------------------------------------
countries_en = pd.read_csv("./Sources/countries/countries_en.csv")
countries_nl = pd.read_csv("./Sources/countries/countries_nl.csv")

# Clean countries files ---------------------------------------------------
countries_en.rename(columns = {
  'name': 'country_name_en',
  'alpha2': 'country_alpha2',
  'alpha3': 'country_alpha3'
  }, 
  inplace = True)
  
countries_nl.rename(columns = {'name': 'country_name_nl'}, inplace = True)
countries_nl = countries_nl.drop(['alpha2', 'alpha3'], axis = 1)

countries = pd.merge(countries_nl, countries_en, on = "id", how = "left")
