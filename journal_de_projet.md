# Ce projet IA va prédire si un étudiant va échouer

J'ai configurer l'api pour qu'elle fasse les transactions nécessaires pour l'application


# 22 Novembre 2025
# 1. Création de la fonction qui chargera le modèle 

Le fichier 'charger_models.py' permet de charger le code avec modèle finale qui est l'arbre de décision.


# 2. Création d'un nouvel environnement python pour déployer notre API

L'environnement se nomme .projetIA_2025


# 3 organisation de l'environnement de l'API pour effectuer le projet

Création de dossier et fichier pour etre prêt à déployer l'API


# 23 novembre 2025
# 4 corriger les types variable a utilise
Certain variables ont du passer de float à int


# 23 novembre 2025
# 5 définition du fichier test_api

Ce fichier me permettra de savoir si mon API fonctionne.


# 24 novembre 2025
# 6 chargement de la liste des colonnes utilisées à l'entrainement (X_train.columns)

Les colonnes d'entrainements situés dans le modèle 'features.pkl' sont utilisée pour s'assurer que notre API utilise les colonnes encodés

# 24 novembre 2025
# 7 seuil de d'échec
Définition du seuil d'échec pour s'assurer que modèle prédit bien si l'étudiant va échouer malgré le déséquilibre des données.


# 24 novembre 2025
# 8 Dockerfile

Création de l'image du docker avec le 'Dockerfile'


# 24 novembre 2025 
# 9 test de différent point d'accès

Les test sont concluent.


# 25 novembre 2025
# Problèmes de prédiction

Avant les prédictions démontrait que l'étudiant va réussir, alors qu'il aurait dû démontrer qu'il allait échoué, ce qui était causé par un déséquilibre des données, donc j'ai dû construire un seuil d'échec pour résoudre ce problème.

Il y avait aussi le problème de l'environnement que j'avais du mal à me connecter donc j'ai créé un nouvel environnement (.projetIA_2025).

