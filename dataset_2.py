# This scripts cleans and merges the relevant files in ./sources
# Sebastiaan Looijen, april 2021

# import libraries --------------------------------------------------------
import pandas as pd

# read core.csv -----------------------------------------------------------
core = pd.read_csv("./core.csv")

# controle variable: GDP stock --------------------------------------------
GDP_stock = pd.read_csv("./sources/GDP_stock/GDP_stock.csv", skiprows=4)
GDP_stock.rename(
        columns={
            'Country Name': 'country_name_en',
            'Country Code': 'country_alpha3'
            }, 
        inplace=True
        )
GDP_stock = GDP_stock.drop(
        ['Indicator Name', 'Indicator Code', '2020', 'Unnamed: 65'],
        axis=1
        )
GDP_stock= pd.melt(
        GDP_stock,
        id_vars=["country_name_en", "country_alpha3"],
        var_name="year",
        value_name="GDP_stock"
        )
GDP_stock['key_alpha3'] = (
        GDP_stock['country_alpha3'].str.lower()
        + GDP_stock['year'].astype(str)
        )
GDP_stock = GDP_stock[['key_alpha3', 'GDP_stock']]

# controle variable: distance ---------------------------------------------
geodist = pd.read_csv("./sources/geodist/geodist.csv")
geodist.query("iso_o == 'NLD'", inplace=True)
