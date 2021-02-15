# This scripts cleans and merges files in ./Sources
# Sebastiaan Looijen, february 2021

# import libraries
import numpy as np
import pandas as pd

# key: country names 
countries_en = pd.read_csv("./Sources/Countries/countries_en.csv")
countries_en.rename(
        columns = {
            'name': 'country_name_en',
            'alpha2': 'country_alpha2',
            'alpha3': 'country_alpha3'},
        inplace = True)
  
countries_nl = pd.read_csv("./Sources/Countries/countries_nl.csv") 
countries_nl.rename(columns = {'name': 'country_name_nl'}, inplace = True)
countries_nl = countries_nl.drop(['alpha2', 'alpha3'], axis = 1)

countries = pd.merge(countries_nl, countries_en, on = "id", how = "left")
countries.rename(columns = {'id': 'country_id'}, inplace = True)

countries['country_name_nl'] = countries['country_name_nl'].replace(
  ['Micronesia',
  'Verenigde Staten'],
  ['Micronesië',
  'Verenigde Staten van Amerika'])

# dependent variable: immigrants
immigrants = pd.read_csv("./Sources/Migration/migrants_nl.csv", sep = ";")
immigrants = immigrants.drop(['ID', 'Geslacht', 'Geboorteland'], axis = 1)
immigrants['Perioden'] = immigrants['Perioden'].str[:4]
immigrants.rename(
        columns = {
            'LandVanHerkomstVestiging': 'Key',
            'Perioden': 'year',
            'Immigratie_1': 'immigrants'},
        inplace = True)
  
metadata = pd.read_csv("./Sources/Migration/metadata.csv", sep = "\t")
immigrants = pd.merge(immigrants, metadata, on = "Key", how = "left")

immigrants = immigrants.drop(['Key'], axis = 1)
immigrants.rename(columns = {'Title': 'country_name_nl'}, inplace = True)
immigrants = immigrants.reindex(
        columns = [
            'country_name_nl', 
            'year', 
            'immigrants'])
            
immigrants['country_name_nl'] = immigrants['country_name_nl'].replace(
  ['Bosnië-Herzegovina',
  'Congo',
  'Congo (Democratische Republiek)',
  'Filippijnen',
  'Katar',
  'Macedonië',
  'Marshall-eilanden',
  'Timor Leste',
  'Uganda'],
  ['Bosnië en Herzegovina',
  'Congo-Brazzaville',
  'Congo-Kinshasa',
  'Filipijnen',
  'Qatar',
  'Noord-Macedonië',
  'Marshalleilanden',
  'Oost-Timor',
  'Oeganda'])            

# independent variable: FDI
FDI = pd.read_csv("./Sources/FDI/FDI_FLOW_PARTNER.csv")
FDI.query("FLOW == 'OUT' and CUR == 'USD' and COU == 'NLD'", inplace = True)
FDI = FDI[['PC', 'Partner country', 'Year', 'Value']]
FDI.rename(
    columns = {
        'PC': 'country_alpha3', 
        'Partner country': 'country_name_en',
        'Value': 'FDI'},
    inplace = True)

# create initial data set
core = pd.merge(immigrants, countries, on = "country_name_nl", how = "inner")
