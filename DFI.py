# This scripts cleans and merges all the files in ./Sources
# Sebastiaan Looijen, february 2021

# Import libraries --------------------------------------------------------
import pandas as pd

# Country names ----------------------------------------------------------- 
countries_en = pd.read_csv("./Sources/Countries/countries_en.csv")
countries_en.rename(
        columns = {
            'name': 'country_name_en',
            'alpha2': 'country_alpha2',
            'alpha3': 'country_alpha3'
            },
        inplace = True
        )
  
countries_nl = pd.read_csv("./Sources/Countries/countries_nl.csv") 
countries_nl.rename(columns = {'name': 'country_name_nl'}, inplace = True)
countries_nl = countries_nl.drop(['alpha2', 'alpha3'], axis = 1)

countries = pd.merge(countries_nl, countries_en, on = "id", how = "left")
countries.rename(columns = {'id': 'country_id'}, inplace = True) 

# MigrantsNL --------------------------------------------------------------
immigrants_nl = pd.read_csv("./Sources/MigrantsNL/migrantsNL.csv", sep = ";")
migrantsNL = migrantsNL.drop(['ID', 'Geslacht', 'Geboorteland'], axis = 1)
migrantsNL['Perioden'] = migrantsNL['Perioden'].str[:4]
migrantsNL.rename(
        columns = {
            'LandVanHerkomstVestiging': 'Key',
            'Perioden': 'year',
            'Immigratie_1': 'migrantsNL'
            },
        inplace = True
        )
  
metadata = pd.read_csv("./Sources/MigrantsNL/metadata.csv", sep = "\t")
migrantsNL = pd.merge(migrantsNL, metadata, on = "Key", how = "left")

migrantsNL = migrantsNL.drop(['Key'], axis = 1)
migrantsNL.rename(columns = {'Title': 'country_name_nl'}, inplace = True)
migrantsNL = migrantsNL.reindex(
        columns = [
            'country_name_nl', 
            'year', 
            'migrantsNL'
            ]
        )
