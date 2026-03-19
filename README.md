# Variants-Genomiques

Explorateur interactif de variants génomiques pathogènes basé sur les données **ClinVar (NCBI)**.

L’objectif de cette application est simple : permettre d’explorer, filtrer et comprendre des variants génétiques à partir de données réelles, via une interface visuelle.

## Lancer l'application

```bash
streamlit run ./app/app.py
```

## Accès à l'application

L’application est maintenant disponible en ligne :
[Accéder à l’application](https://variants-genomiques-jdvh6xxymstnbxtspqirsr.streamlit.app/)

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


## TODO
- Re-nettoyer les données et faire un pipeline automatisé
- Réduire le volume
- Ajouter plus de contexte biologique sur la page information de variante
- En parlant de page, diviser en pages streamlit
- Changer les filtres pour qu'ils ne recherchent pas toute la page
- Ajouter des visualisations supplémentaires
- Permettre de chercher d'autres génomes, pas que humains, en ajoutant votre propre fichier

Icon ADN crée par Freepik - Flaticon