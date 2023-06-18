from dagster import AssetIn, asset, file_relative_path
from dagstermill import define_dagstermill_asset

import pandas as pd
from pandas import DataFrame

@asset
def acteurs() -> DataFrame:
    return pd.read_csv('out/acteurs.csv')

@asset
def organes() -> DataFrame:
    return pd.read_csv('out/organes.csv')

@asset
def amendements() -> DataFrame:
    return pd.read_csv('out/amendements.csv')

@asset
def reunions() -> DataFrame:
    return pd.read_csv('out/reunions.csv')

@asset
def interventions() -> DataFrame:
    return pd.read_csv('out/interventions.csv')

@asset
def scrutins() -> DataFrame:
    return pd.read_csv('out/scrutins.csv')

@asset
def votes() -> DataFrame:
    return pd.read_csv('out/votes.csv')


# references_nb = define_dagstermill_asset(
#     name="references",
#     notebook_path=file_relative_path(__file__, "../1_prep_references.ipynb"),
#     # analyse-l16-votes/an-l16/1_prep_references.ipynb
# )