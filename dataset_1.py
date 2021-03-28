# This scripts cleans and merges all the files in ./Sources
# Sebastiaan Looijen, february 2021

# Import libraries --------------------------------------------------------
import pandas as pd

# Read core.csv -----------------------------------------------------------
core = pd.read_csv("./core.csv")

# Controle variable: population growth ------------------------------------
popgrowth = pd.read_csv("./sources/pop_growth/POPGROW.csv", skiprows=4)
popgrowth.rename(
      columns={
          'Country Name': 'country_name_en',
          'Country Code': 'country_alpha3'}, 
          inplace=True
          )
popgrowth = popgrowth.drop(['Indicator Name', 'Indicator Code'], axis=1)
popgrowth = pd.melt(
      popgrowth,
          id_vars=["country_name_en", "country_alpha3"],
          var_name="year",
          value_name="population_growth"
          )

#TODO: controle variable: GDP per capita
#TODO: controle variable: GDP growth
