# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% tags=[]
import pandas as pd

# %% tags=[]
organes = (pd.read_csv('out/organes.csv'))
votes = pd.read_csv('out/votes.csv')

# %% tags=[]
nupes = (
    organes
    .query('libelle.str.contains("NUPES") or libelle.str.contains("France insoumise")')
)

nupes

# %% tags=[]
alignements = (
    votes
#    .query('organe.isin(@nupes.uid)')
    .groupby(['scrutin', 'organe'])
    .agg({
        'groupe_majorite': 'first'
    })
    .reset_index()
    .assign(
        organe = lambda df: df.join(organes.set_index('uid'), on='organe')[['libelle']]
    )
    .pivot_table(
        index="scrutin",
        columns="organe",
        values="groupe_majorite",
        aggfunc= lambda x: x
    )
)

alignements


# %% tags=[]
def get_covotes(df, groupe):
    return (
        df
        .T
        .fillna('non votant')
        .pipe( lambda df: (
            df
            .eq(df.loc[groupe])
        ))
        .sum(axis=1)
        .to_frame()
        .rename(columns={0: groupe})
    )

covotes = pd.concat([ get_covotes(alignements, g).T for g in alignements.T.index ])

covotes

# %%
import numpy as np

# %%
import scipy
import scipy.cluster.hierarchy as sch

def cluster_corr(corr_array, inplace=False):
    """
    Rearranges the correlation matrix, corr_array, so that groups of highly 
    correlated variables are next to eachother 
    
    Parameters
    ----------
    corr_array : pandas.DataFrame or numpy.ndarray
        a NxN correlation matrix 
        
    Returns
    -------
    pandas.DataFrame or numpy.ndarray
        a NxN correlation matrix with the columns and rows rearranged
    """
    pairwise_distances = sch.distance.pdist(corr_array)
    linkage = sch.linkage(pairwise_distances, method='complete')
    cluster_distance_threshold = pairwise_distances.max()/2
    idx_to_cluster_array = sch.fcluster(linkage, cluster_distance_threshold, 
                                        criterion='distance')
    idx = np.argsort(idx_to_cluster_array)
    
    if not inplace:
        corr_array = corr_array.copy()
    
    if isinstance(corr_array, pd.DataFrame):
        return corr_array.iloc[idx, :].T.iloc[idx, :]
    return corr_array[idx, :][:, idx]


# %% tags=[]
(
    cluster_corr(covotes)
    .div(
        len(alignements.index), axis=0
    )
    .replace(1, np.nan)
    .style
        .format('{:,.1%}'.format)
        .background_gradient(
            cmap='PiYG',
            vmin=0,
            vmax=1
        )
)

# %%
(
    cluster_corr(
        covotes
        .div(
            len(alignements.index), axis=0
        )
    )
    .replace(1, np.nan)
    .style
        .format('{:,.1%}'.format)
        .background_gradient(
            cmap='PiYG',
            vmin=0,
            vmax=1
        )
)

# %%
organes_pca = pd.read_csv('out/organes_pca.csv')

organes_pca

# %%
(
    covotes[organes_pca.libelle].loc[organes_pca.libelle]
    .style
        .background_gradient(
            cmap='PiYG',
        )
)

# %%
covotes[organes_pca.libelle].loc[organes_pca.libelle].to_csv('out/covotes-organes.csv')

# %%
(
    covotes[organes_pca.libelle].loc[organes_pca.libelle]
    .div(
        len(alignements.index), axis=0
    )
    .replace(1, np.nan)
    .style
        .format('{:,.1%}'.format)
        .background_gradient(
            cmap='PiYG',
            # vmin=0,
            # vmax=1
            axis=1
        )
)

# %%
