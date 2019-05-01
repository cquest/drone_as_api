# API REST/json d'interrogation des zones de restriction de vol pour les drones de loisir

Zones soumises à interdictions ou à restrictions pour l’usage, à titre de loisir, d’aéronefs télépilotés (ou drones), sur le territoire métropolitain.

Ces données intègrent partiellement les interdictions s’appuyant sur des données publiées hors de l’AIP (Aeronautical Information Publication) et ne couvrent pas les interdictions temporaires.
Elles sont basées sur l’arrêté « espace » du 30 mars 2017.

Les zones avec la limite général à 150m/sol sont calculée en retranchant les zones restreintes des polygones simplifiés des départements.


## Source et millésime

Source des données: SIA/DGAC

Millésime des données: 2018-11


## Informations complémentaires

La représentation des zones soumises à interdictions ou à restrictions n’engage pas la responsabilité des producteurs de la donnée.
Le contour des agglomérations est fourni à titre purement indicatif.
Il est rappelé que le survol d'un fleuve ou d'un parc en agglomération est interdit.

Consulter ces données ou une carte ne dispense pas de connaitre la réglementation, de l’appliquer avec discernement et de rester prudent en toute occasion.

Plus d'informations disponibles sur https://www.ecologique-solidaire.gouv.fr/modeles-reduits-et-drones-loisir

La dernière version visualisable est disponible sur https://www.geoportail.gouv.fr/donnees/restrictions-pour-drones-de-loisir


Aucune licence n'étant clairement indiquée pour ces données, on peut considérer qu'elles relèvent du cadre général du Code des Relations entre le Public et l'Administration (CRPA) correspondant à la Licence Ouverte 2.0.


# Utilisation de l'API

La recherche se fait géographiquement, avec possibilité de filtrer les réponses:
- lat/lon/rayon: latitude/longitude autour de laquelle chercher dans un rayon donné (par défaut 1000m)
- limite: filtre sur la limite en hauteur de vol
- limite_min : filtre sur la limite minimale de hauteur de vol

Exemples:
- https://api.cquest.org/drone?lat=47.9&lon=3.4 : toutes les zones dans un rayon de 1000m
- https://api.cquest.org/drone?lat=47.9&lon=3.4&rayon=5000&limite=50 : toutes les zones avec une hauteur limite de 50m/sol à 5km à la ronde
- https://api.cquest.org/drone?lat=48.85&lon=2.35&rayon=30000&limite_min=100 : zones les plus proches du centre de Paris avec un hauteur limite mini de 100m

Infos retournées:
- format geojson
- properties:
  - limite_alti_m : hauteur maximale de vol autorisée (en m)
  - distance_m : distance du point initial à la zone en question (en m), 0 si l'on se trouve dans la zone.
  - cap_deg : cap vers le points le plus proche de la zone (en degrés), null si l'on se trouve dans la zone.

Les résultats sont triés par distance croissante, la zone la plus proche est donc la première retournée.


# Exemple de carte dynamique s'appuyant sur l'API

Il s'agit d'une carte uMap interrogeant l'API de façon dynamique:

https://umap.openstreetmap.fr/fr/map/restrictions-de-vol-pour-drones-de-loisir_321092
