# This scripts cleans and merges all the files in ./sources 
# Sebastiaan Looijen, april 2021 

# import libraries --------------------------------------------------------
import pandas as pd

# read core.csv -----------------------------------------------------------
core = pd.read_csv("./core.csv")

# controle variable: population growth ------------------------------------
pop_growth = pd.read_csv("./sources/pop_growth/POPGROW.csv", skiprows=4)
pop_growth.rename(
        columns={
            'Country Name': 'country_name_en',
            'Country Code': 'country_alpha3'
            }, 
        inplace=True
        )
pop_growth = pop_growth.drop(['Indicator Name', 'Indicator Code'], axis=1)
pop_growth = pd.melt(
        pop_growth,
        id_vars=["country_name_en", "country_alpha3"],
        var_name="year",
        value_name="population_growth"
        )
pop_growth['key_alpha3'] = (
        pop_growth['country_alpha3'].str.lower() 
        + pop_growth['year'].astype(str)
        )
pop_growth = pop_growth[['key_alpha3', 'population_growth']]

# controle variable: GDP per capita ---------------------------------------
GDP_capita = pd.read_csv(
        "./sources/GDP_per_capita/GDP_per_capita.csv", 
        skiprows=4
        )
GDP_capita.rename(
        columns={
            'Country Name': 'country_name_en',
            'Country Code': 'country_alpha3'
            }, 
        inplace=True
        )
GDP_capita = GDP_capita.drop(
        ['Indicator Name', 'Indicator Code', '2020', 'Unnamed: 65'],
        axis=1
        )
GDP_capita= pd.melt(
        GDP_capita,
        id_vars=["country_name_en", "country_alpha3"],
        var_name="year",
        value_name="GDP_per_capita"
        )
GDP_capita['key_alpha3'] = (
        GDP_capita['country_alpha3'].str.lower() 
        + GDP_capita['year'].astype(str)
        )
GDP_capita = GDP_capita[['key_alpha3', 'GDP_per_capita']]

# controle variable: GDP growth -------------------------------------------
GDP_growth = pd.read_csv("./sources/GDP_growth/GDP_growth.csv", skiprows=4)
GDP_growth.rename(
        columns={
            'Country Name': 'country_name_en',
            'Country Code': 'country_alpha3'
            }, 
        inplace=True
        )
GDP_growth = GDP_growth.drop(
        ['Indicator Name', 'Indicator Code', '2020', 'Unnamed: 65'],
        axis=1
        )
GDP_growth = pd.melt(
        GDP_growth,
        id_vars=["country_name_en", "country_alpha3"],
        var_name="year",
        value_name="GDP_growth"
        )
GDP_growth['key_alpha3'] = (
        GDP_growth['country_alpha3'].str.lower() 
        + GDP_growth['year'].astype(str)
        )
GDP_growth = GDP_growth[['key_alpha3', 'GDP_growth']]
       
# merge datasets ----------------------------------------------------------
dataset_1 = pd.merge(popgrowth, GDPcapita, on="key_alpha3", how="left")
dataset_1 = pd.merge(dataset_1, GDPgrowth, on="key_alpha3", how="left")
dataset_1 = pd.merge(core, dataset_1, on="key_alpha3", how="left")
