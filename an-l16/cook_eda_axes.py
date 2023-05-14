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

# %%
import pandas as pd

# %%
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt

# %%
loyautes = pd.read_csv('out/loyautes.csv', index_col='acteurRef')

# %%
acteurs = (
    pd
    .read_csv('out/votes.csv')
    .join(loyautes[['loyaute']], on='acteurRef')
    .assign(
        loyaute = lambda df: 1 - df.loyaute.fillna(0)
    )
)

acteurs

# %%
X = (
    acteurs
    .assign(
        position = lambda df: df.position.replace({'contre': -1, 'pour': 1, 'abstention': 0 })
    )
    .pivot_table(
        index='acteurRef',
        columns='scrutin',
        values='position'
    )
    .fillna(0)
)

X

# %%
pca = PCA(n_components=2)
X_r = pca.fit(X.values).transform(X.values)

# %%
pca.explained_variance_ratio_

# %%
len(X_r)

# %%
organes = pd.read_csv('out/organes.csv')

# %%
scrutins_vecteur = (
    X.reset_index()
    .join(acteurs.drop_duplicates(subset='acteurRef').set_index('acteurRef'), on='acteurRef')
    .join(organes.set_index('uid'), on='organe')
    .set_index('acteurRef')
)

scrutins_vecteur

# %%
mapping = (
    pd
    .DataFrame(X_r, columns=["axe 1", "axe 2"])
    .join(
        X.reset_index()
        .join(acteurs.drop_duplicates(subset='acteurRef').set_index('acteurRef'), on='acteurRef')
        .join(organes.set_index('uid'), on='organe')
    )
    .set_index('acteurRef')
)

mapping

# %%
axe = (
    mapping
    [['axe 1','axe 2', 'organe']]
    .groupby('organe')
    .median()
    .sort_values('axe 2')
)

(
    axe
    .join(organes.set_index('uid'))
    .set_index('libelle')
)

# %%
(
    axe
    .join(organes.set_index('uid'))
    .set_index('libelle')
    .to_csv('out/organes_pca.csv')
)

# %%
mapping.to_csv('out/axes_vecteur-scrutins_pca.csv')

# %%
fig, ax = plt.subplots()

(
    axe
    .join(organes.set_index('uid'))
    .plot
    .scatter(
        x="axe 2",
        y="axe 1",
        c="couleurAssociee",
        alpha=0.3,
        s=5000,
        ax=ax,
    )
)

(
    mapping
    .plot
    .scatter(
        x="axe 2",
        y="axe 1",
        s=12,
        #a="loyaute",
        alpha= 0.7, #1-loyautes.loyaute.fillna(0),
        c="couleurAssociee",
        figsize=(15,10),
        ax=ax
    )
)

plt.legend(
    handles=[
        plt.Line2D([0], [0], marker='o', color='w', label=org['libelle'], markerfacecolor=org['couleurAssociee'], markersize=15)
        for org in axe.join(organes.set_index('uid')).to_records()
    ],
    loc='upper center',
    bbox_to_anchor=(0.5, -0.1),
    ncol=3
)

ax.axis('off')

plt.savefig('graphics/acteurs_pca_scrutins.png', bbox_inches='tight')

plt.show()

# %%
axe.join(organes.set_index('uid'))

# %%
groupes = pd.CategoricalDtype(categories=axe.join(organes.set_index('uid')).libelle, ordered=True)
groupes

# %%
fig, ax = plt.subplots()

(
    mapping
    [['axe 2', 'libelle', 'couleurAssociee']]
    .assign(
        libelle = lambda df: df.libelle.astype(groupes)
    )
    .reset_index(drop=True)
    .plot
    .box(
        by="libelle",
        vert=False,
        ax=ax,
        #xlim=[-20, 20]
    )
)

ax.set_yticklabels(axe.join(organes.set_index('uid')).libelle)

plt.show()

# %%
fig, ax = plt.subplots()

(
    mapping
    [['axe 1', 'libelle', 'couleurAssociee']]
    .assign(
        libelle = lambda df: df.libelle.astype(groupes)
    )
    .reset_index(drop=True)
    .plot
    .box(
        by="libelle",
        vert=False,
        ax=ax
    )
)

ax.set_yticklabels(axe.join(organes.set_index('uid')).libelle)

plt.show()
