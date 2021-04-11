# This scripts cleans and merges the relevant files in ./sources
# Sebastiaan Looijen, february 2021

# import libraries --------------------------------------------------------
import pandas as pd

# key: country names ------------------------------------------------------
countries_en = pd.read_csv("./sources/countries/countries_en.csv")
countries_en.rename(
        columns={
            'name': 'country_name_en',
            'alpha2': 'country_alpha2',
            'alpha3': 'country_alpha3'
            },
        inplace=True
        )

countries_nl = pd.read_csv("./sources/countries/countries_nl.csv")
countries_nl.rename(columns={'name': 'country_name_nl'}, inplace=True)
countries_nl = countries_nl.drop(['alpha2', 'alpha3'], axis=1)
countries = pd.merge(countries_nl, countries_en, on="id", how="left")
countries.rename(columns={'id': 'country_id'}, inplace=True)
countries['country_name_nl'] = countries['country_name_nl'].replace(
        [
            'Micronesia',
            'Verenigde Staten'
        ],
        [
            'Micronesië',
            'Verenigde Staten van Amerika'
        ]
        )
countries = countries.drop(['country_id'], axis=1)

# dependent variable: immigrants ------------------------------------------
immigrants = pd.read_csv("./sources/migration/migrants_nl.csv", sep=";")
immigrants = immigrants.drop(['ID', 'Geslacht', 'Geboorteland'], axis=1)
immigrants['Perioden'] = immigrants['Perioden'].str[:4]
immigrants.rename(
        columns={
            'LandVanHerkomstVestiging': 'Key',
            'Perioden': 'year',
            'Immigratie_1': 'immigrants'
            },
        inplace=True
        )

metadata = pd.read_csv("./sources/migration/metadata.csv", sep="\t")
immigrants = pd.merge(immigrants, metadata, on="Key", how="left")

immigrants = immigrants.drop(['Key'], axis=1)
immigrants.rename(columns={'Title': 'country_name_nl'}, inplace=True)
immigrants = immigrants.reindex(
        columns=[
            'country_name_nl',
            'year',
            'immigrants'
            ]
        )

immigrants['country_name_nl'] = immigrants['country_name_nl'].replace(
        [
            'Bosnië-Herzegovina',
            'Congo',
            'Congo (Democratische Republiek)',
            'Filippijnen',
            'Katar',
            'Macedonië',
            'Marshall-eilanden',
            'Timor Leste',
            'Uganda'
        ],
        [
            'Bosnië en Herzegovina',
            'Congo-Brazzaville',
            'Congo-Kinshasa',
            'Filipijnen',
            'Qatar',
            'Noord-Macedonië',
            'Marshalleilanden',
            'Oost-Timor',
            'Oeganda'
        ]
        )

# independent variable: FDI -----------------------------------------------
FDI = pd.read_csv("./sources/FDI/FDI_FLOW_PARTNER.csv")
FDI.query("FLOW == 'OUT' and CUR == 'USD' and COU == 'NLD'", inplace=True)
FDI = FDI[['PC', 'Partner country', 'Year', 'Value']]
FDI.rename(
        columns={
            'PC': 'country_alpha3',
            'Partner country': 'country_name_en',
            'Year': 'year',
            'Value': 'FDI'
            },
        inplace=True
        )
FDI['country_name_en'] = FDI['country_name_en'].replace(
        [
            'Bolivia',
            'Cape Verde',
            'Congo, the Democratic Republic of the',
            'Czech Republic',
            'Iran, Islamic Republic of',
            "Korea, Dem. People's Republic of (North Korea)",
            'Korea, Republic of (South Korea)',
            'Micronesia, Federal States of',
            'Montenegro, Republic of',
            'NewZealand',
            'Papua New Guine',
            'Serbia, Republic of',
            'SriLanka',
            'St. Vincent and the Grenadines',
            'St. Kitts and Nevis',
            'St. Lucia',
            'Swaziland',
            'Timor_Leste',
            'United Kingdom',
            'United States',
            'Venezuela'
        ],
        [
            'Bolivia (Plurinational State of)',
            'Cabo Verde',
            'Congo, Democratic Republic of the',
            'Czechia',
            'Iran (Islamic Republic of)',
            "Korea (Democratic People's Republic of)",
            'Korea, Republic of',
            'Micronesia (Federated States of)',
            'Montenegro',
            'New Zealand',
            'Papua New Guinea',
            'Serbia',
            'Sri Lanka',
            'Saint Vincent and the Grenadines',
            'Saint Kitts and Nevis',
            'Saint Lucia',
            'Eswatini',
            'Timor-Leste',
            'United Kingdom of Great Britain and Northern Ireland',
            'United States of America',
            'Venezuela (Bolivarian Republic of)'
        ]
        )

FDI['key_name_en'] = FDI['country_name_en'] + FDI['year'].astype(str)
FDI = FDI[['key_name_en', 'FDI']]

# create initial dataset --------------------------------------------------
core = pd.merge(immigrants, countries, on="country_name_nl", how="inner")
core['key_name_en'] = core['country_name_en'] + core['year']
core['key_alpha3'] = core['country_alpha3'] + core['year']
core = core.reindex(
        columns=[
            'country_name_en',
            'country_name_nl',
            'country_alpha2',
            'country_alpha3',
            'year',
            'key_name_en',
            'key_alpha3',
            'immigrants'
            ]
        )

core = pd.merge(core, FDI, on='key_name_en', how='left')

# write file --------------------------------------------------------------
core.to_csv("~/Documents/migrationFDI/core.csv", index=False)
