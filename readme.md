# analyse des données ouvertes de l'Assemblée Nationale

Ce dépôt contient :

* les notebooks permettant la production de données et de graphqiques pour des publications. Par exemple :
  * [analyse en composantes principales des comportements de votes](https://github.com/taniki/assemblee-nationale/blob/main/an-l16/2_cook_eda_axes.ipynb)
  * [compilation et indexation des prises de parole](https://github.com/taniki/assemblee-nationale/blob/main/an-l16/2_cook_synthese_interruptions.ipynb) 
* les notebooks ayant permis la production de données exploratoires. Par exemple :
  * [détection d'entitées nommées](https://github.com/taniki/assemblee-nationale/blob/main/an-l16/cook_interventions_ner.ipynb)
  * [topic modelling](https://github.com/taniki/assemblee-nationale/blob/main/an-l16/cook_interventions_topic_modelling.ipynb) 
* une [automatisation des différents traitements](https://github.com/taniki/assemblee-nationale/blob/main/an-l16/__init__.py) avec une tuyauterie [dagster] afin de reproduire et mettre à jour les productions

[dagster]: https://dagster.io

## publications

* [Un an de votes « attrape-tout » pour le RN](https://www.mediapart.fr/journal/politique/220623/un-de-votes-attrape-tout-pour-le-rn)
* [Nupes : à l’Assemblée, les chiffres prouvent que le groupe vit (plutôt) bien](https://www.mediapart.fr/journal/politique/130523/nupes-l-assemblee-les-chiffres-prouvent-que-le-groupe-vit-plutot-bien)
* [spatialisation des députés avec une analyse en composantes principales](https://data.11d.im/foodcourt/votes-an/pca-deputes)
