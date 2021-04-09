# This scripts cleans and merges all the files in ./sources 
# Sebastiaan Looijen, april 2021 

# import libraries --------------------------------------------------------
import pandas as pd

# read core.csv -----------------------------------------------------------
core = pd.read_csv("./core.csv")

# controle variable: population growth ------------------------------------
popgrowth = pd.read_csv("./sources/pop_growth/POPGROW.csv", skiprows=4)
popgrowth.rename(
        columns={
            'Country Name': 'country_name_en',
            'Country Code': 'country_alpha3'
            }, 
        inplace=True
        )
popgrowth = popgrowth.drop(['Indicator Name', 'Indicator Code'], axis=1)
popgrowth = pd.melt(
        popgrowth,
        id_vars=["country_name_en", "country_alpha3"],
        var_name="year",
        value_name="population_growth"
        )
popgrowth['key_alpha3'] = (
        popgrowth['country_alpha3'].str.lower() 
        + popgrowth['year'].astype(str)
        )
popgrowth = popgrowth[['key_alpha3', 'population_growth']]

# controle variable: GDP per capita ---------------------------------------
GDPcapita = pd.read_csv(
        "./sources/GDP_per_capita/GDP_per_capita.csv", 
        skiprows=4
        )
GDPcapita.rename(
        columns={
            'Country Name': 'country_name_en',
            'Country Code': 'country_alpha3'
            }, 
        inplace=True
        )
GDPcapita = GDPcapita.drop(
        ['Indicator Name', 'Indicator Code', '2020', 'Unnamed: 65'],
        axis=1
        )
GDPcapita= pd.melt(
        GDPcapita,
        id_vars=["country_name_en", "country_alpha3"],
        var_name="year",
        value_name="GDP_per_capita"
        )
GDPcapita['key_alpha3'] = (
        GDPcapita['country_alpha3'].str.lower() 
        + GDPcapita['year'].astype(str)
        )
GDPcapita = GDPcapita[['key_alpha3', 'GDP_per_capita']]

#TODO: controle variable: GDP growth
#TODO: merge all
