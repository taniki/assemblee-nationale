from dagster import (
    load_assets_from_package_module,
    Definitions,
    file_relative_path,
    asset,
    job,
    op,
    AssetIn,
    AssetOut,
    multi_asset,
    Out
)

from dagstermill import (
    ConfigurableLocalOutputNotebookIOManager,
    define_dagstermill_op,
    define_dagstermill_asset
)

import pandas as pd

from pandas import DataFrame

from . import assets

fetch_data = define_dagstermill_op(
    name='fetch_data',
    notebook_path=file_relative_path(__file__, './0_prep_download_unzip.ipynb'),
    output_notebook_name="fetch_data_execution",
)


prep_references = define_dagstermill_op(
    name='prep_references',
    #group_name="prep",
    notebook_path=file_relative_path(__file__, './1_prep_references.ipynb'),
    output_notebook_name="prep_amendements_execution",
    outs={
        'acteurs': Out(DataFrame),
        'organes': Out(DataFrame)
    }
)

prep_reunions = define_dagstermill_op(
    name='prep_reunions',
    #group_name="prep",
    notebook_path=file_relative_path(__file__, './1_prep_reunions.ipynb'),
    output_notebook_name="prep_reunions_execution",
    outs={
        'reunions': Out(DataFrame),
    }
)

prep_amendements = define_dagstermill_op(
    name='prep_amendements',
    #group_name="prep",
    notebook_path=file_relative_path(__file__, './1_prep_amendements.ipynb'),
    output_notebook_name="prep_amendements_execution",
    outs={
        'amendements': Out(DataFrame),
    }
)

prep_interventions = define_dagstermill_op(
    name='prep_interventions',
    #group_name="prep",
    notebook_path=file_relative_path(__file__, './1_prep_interventions.ipynb'),
    output_notebook_name="prep_interventions_execution",
    outs={
        'interventions': Out(DataFrame),
    }
)

prep_scrutins_votes = define_dagstermill_op(
    name='prep_scrutins_votes',
    #group_name="prep",
    notebook_path=file_relative_path(__file__, './1_prep_scrutins_votes.ipynb'),
    output_notebook_name="prep_scrutins_votes_execution",
    outs={
        'scrutins': Out(DataFrame),
        'votes': Out(DataFrame),
    }
)

@job()
def get_ingredients():
    fetch_data()


@job()
def prep_all():
    acteurs, organes, _ = prep_references()
    amendements, _ = prep_amendements()
    reunions, _ = prep_reunions()
    interventions, _ = prep_interventions()
    scrutins, votes, _ = prep_scrutins_votes()

pca_votes_nb = define_dagstermill_asset(
    name="pca_votes",
    group_name="eda",
    notebook_path=file_relative_path(__file__, "2_cook_eda_axes.ipynb"),
    ins={
        'acteurs': AssetIn('acteurs'),
        'organes': AssetIn('organes'),
        'votes': AssetIn('votes'),
    }
)

eda_rn_nb = define_dagstermill_asset(
    name="20223_rn",
    group_name="articles",
    notebook_path=file_relative_path(__file__, "2_cook_eda_rn.ipynb"),
    ins={
        'acteurs': AssetIn('acteurs'),
        'organes': AssetIn('organes'),
        'amendements': AssetIn('amendements'),
        'reunions': AssetIn('reunions'),
        'interventions': AssetIn('interventions'),
        'scrutins': AssetIn('scrutins'),
        'votes': AssetIn('votes'),
        'pca_votes': AssetIn('pca_votes'),
    }
)

# @multi_asset(
#     outs={
#         "acteurs": AssetOut(),
#         "organes": AssetOut(),
#     }
# )
# def acteurs_organes():
#     acteurs, organes, _ = prep_references()
#     return acteurs, organes


defs = Definitions(
    # ops= [
    #     prep_amendements
    # ],
    assets= [
        *load_assets_from_package_module(assets, group_name="ingredients"),
        # acteurs,
        # organes,
        # amendements,
        # reunions,
        # interventions,
        # scrutins,
        # votes,
        pca_votes_nb,
        eda_rn_nb
    ],
    resources={"output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager()},
    jobs=[
        get_ingredients,
        prep_all
    ]
)