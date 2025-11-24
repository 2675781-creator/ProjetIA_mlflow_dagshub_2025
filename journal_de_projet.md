# Ce projet IA va prédire si un étudiant va échouer

J'ai configurer l'api pour qu'elle fasse les transactions nécessaires pour l'application



## 1. Structure du projet

Exemple de structure :

```text
PROJETIA_MLFLOW_DAGSHUB_2025/
|── .projetIA_2025/
|   ├──Include
|   ├──Lib                   # Bibliothèque de l'environnement python
|   ├──Scripts
|   ├──share
|   ├──pyvenv.cfg
├── app/
│   ├── __pycache__.py
│   ├── main.py              # point d'entrée de l'API Flask
│   ├── charger_modele.py    # chargement du modèle
│   └── utilites.py          # fonction log_request(...)
├── code/
|    ├──dictionnaire_donnees.csv
|    ├──Student_prediction version 2.ipynb
|    └──student-por.csv
├── models/
│   └── modele_beton.pkl     # modèle entraîné (sérialisé)
├── test/
│   └── test_api.py          # script de test optionnel
├── requetes_enrg.jsonl      # fichier de log des requêtes (optionnel)
├── requirements.txt         # dépendances minimales pour l’API
├── Dockerfile               # recette de construction de l’image Docker
└── .dockerignore            # fichiers à exclure du build (n'est pas vraiment utilisé dans cette démo)
```

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

Les colonnes d'entrainements situés dans le modèle 'modele_tree.pkl'. Sont utilisée pour s'assurer que notre API utilise les colonnes encodés

# 24 novembre 2025
# 7 seuil de d'échec
Définition du seuil d'échec pour s'assurer que modèle prédit bien si l'étudiant va échouer malgré le déséquilibre des données.


# 24 novembre 2025
# 8 Dockerfile

Création de l'image du docker


# 24 novembre 2025 
# 9 test de différent point d'accès



