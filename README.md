# Variants-Genomiques

Explorateur interactif de variants génomiques pathogènes basé sur les données **ClinVar (NCBI)**.

L’objectif de cette application est simple : permettre d’explorer, filtrer et comprendre des variants génétiques à partir de données réelles, via une interface visuelle.

## Lancer l'application

```bash
streamlit run ./app/app.py
```

## Statut du projet

L’application n’est pas encore disponible en ligne.

Je prévois de la mettre en ligne le 18/03 dans l’après-midi.
Les données étant volumineuses, elles ne peuvent pas être hébergées directement sur GitHub.

Merci pour votre patience ! 
![Sorry !](sorry.png)

## Données

* Source : **ClinVar (NCBI)**
* Référence : génome humain **GRCh37**
* Données : variants pathogènes avec annotations (gènes, maladies, types, etc.)

## Fonctionnalités

* Visualisation globale des variants :
  * distribution par chromosome
  * signification clinique
  * gènes les plus impactés
* Filtres :
  * chromosome
  * type de variant
  * signification clinique
* Exploration de gène :
  * nombre de variants
  * maladies associées
  * types de variants
* Export de données :
  * téléchargement d’échantillons CSV
* Interface fait via Streamlit

## Contexte

Ce projet est avant tout un projet d’apprentissage en bioinformatique.

L’idée était de manipuler des données génétiques réelles pour mieux comprendre, la structure des fichiers comment les nettoyer et les bases de l’analyse de variants.

Il reste encore des améliorations à faire, notamment sur la qualité des données et certaines visualisations, mais le projet pose deja une base.
