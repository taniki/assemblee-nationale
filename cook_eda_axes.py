# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
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
(
    pd
    .DataFrame(X_r, columns=["x", "y"])
    .plot
    .scatter(
        x="x",
        y="y",
        figsize=(15,10)
    )
)

# %%
organes = pd.read_csv('out/organes.csv')

# %%
(
        X.reset_index()
        .join(acteurs.drop_duplicates(subset='acteurRef').set_index('acteurRef'), on='acteurRef')
        .join(organes.set_index('uid'), on='organe')
)

# %%
(
    pd
    .DataFrame(X_r, columns=["x", "y"])
    .join(
        X.reset_index()
        .join(acteurs.drop_duplicates(subset='acteurRef').set_index('acteurRef'), on='acteurRef')
        .join(organes.set_index('uid'), on='organe')
    )
    .plot
    .scatter(
        x="x",
        y="y",
        s=5,
        c="couleurAssociee",
        figsize=(15,10)
    )
)

# %%
(
    pd
    .DataFrame(X_r, columns=["x", "y"])
    .join(
        X.reset_index()
        #[['acteurRef']]
        .join(acteurs.set_index('acteurRef'), on='acteurRef')
        #[['organe']]
        .join(organes.set_index('uid'), on='organe')
        #[['couleurAssociee']]
    )
    .query("y > 10")
    [['libelle']]
)

# %%
axe = (
    pd
    .DataFrame(X_r, columns=["x", "y"])
    .join(
        X.reset_index()
        .join(acteurs.drop_duplicates(subset='acteurRef').set_index('acteurRef'), on='acteurRef')
        .join(organes.set_index('uid'), on='organe')
    )
    [['x','y', 'organe']]
    .groupby('organe')
    .median()
    .sort_values('y')
)

(
    axe
    .join(organes.set_index('uid'))
    .set_index('libelle')
)

# %%
fig, ax = plt.subplots()

(
    axe
    .join(organes.set_index('uid'))
    .plot
    .scatter(
        x="y",
        y="x",
        c="couleurAssociee",
        alpha=0.3,
        s=5000,
        ax=ax,
    )
)

(
    pd
    .DataFrame(X_r, columns=["x", "y"])
    .join(
        X.reset_index()
        .join(acteurs.drop_duplicates(subset='acteurRef').set_index('acteurRef'), on='acteurRef')
        .join(organes.set_index('uid'), on='organe')
    )
    .plot
    .scatter(
        x="y",
        y="x",
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

plt.show()

# %%
axe.join(organes.set_index('uid'))

# %%
groupe_categorie = pd.CategoricalDtype(categories=axe.join(organes.set_index('uid')).libelle, ordered=True)

groupe_categorie

# %%
fig, ax = plt.subplots()

(
    pd
    .DataFrame(X_r, columns=["x", "y"])
    .join(
        X.reset_index()
        .join(acteurs.drop_duplicates(subset='acteurRef').set_index('acteurRef'), on='acteurRef')
        .join(organes.set_index('uid'), on='organe')
    )
    [['y', 'libelle', 'couleurAssociee']]
    .assign(
        libelle = lambda df: df.libelle.astype(groupe_categorie)
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
    pd
    .DataFrame(X_r, columns=["x", "y"])
    .join(
        X.reset_index()
        .join(acteurs.drop_duplicates(subset='acteurRef').set_index('acteurRef'), on='acteurRef')
        .join(organes.set_index('uid'), on='organe')
    )
    [['x', 'libelle', 'couleurAssociee']]
    .assign(
        libelle = lambda df: df.libelle.astype(groupe_categorie)
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

# %%
