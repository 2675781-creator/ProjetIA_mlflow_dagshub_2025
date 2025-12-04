# README – API de prédiction de l'échec des étudiants

## Cette API permet de prédire la probabilité d'échec ou de réussite d'un étudiant.

Ce projet montre comment :

1. Lancer une API de prédiction **en local**
2. Lancer la même API **dans Docker**
3. **Enregistrer les requêtes** dans un fichier
4. **Consulter** ce qui se trouve dans l’image / le conteneur
5. **Arrêter** proprement l’API et les logs
6. **Enregister**  les requête dans Docker
7. Voir ce qu’il y a **dans l’image / le conteneur**
8. Arrêter proprement le conteneur du **docker**
9. Installer et initialiser **Google Cloud SDK**
10. **Déploiement** de l'image de Docker sur Google Cloud
11. **Rôle IAM** recommandés et **création** d'un dépôt Artifact Registry
12. **Activer l'authentification** avec Docker
---

## 0. Prérequis

* Python 3.9.7
* `pip` installé
* **Docker Desktop** installé et en marche (pour la partie Docker)

---

## 1. Structure du projet

Exemple de structure :

```text
PROJETIA_MLFLOW_DAGSHUB_2025/
├──.projetIA_2025           # environnement de l'API
├── app/
│   ├── __pycache__/
│   ├── main.py              # point d'entrée de l'API Flask
│   ├── charger_modele.py    # chargement des modèles
│   └── utilites.py          # fonction log_request(...)
├── code/
│   └── modele_trees.pkl     # modèle entraîné (sérialisé)
|   └── features.pkl         # colonnes que le modèles doit prendre en considération
├── mlruns/                  # environnement mlflows
|   ├──.trash/
|   ├──0/
|   |  └── meta.yaml
|   ├──103492033373399759/
|   ├── 232320979372170434/         
|   └──models/
├── test/
│   └── test_api.py          # script de test optionnel
├── requetes_enrg.jsonl      # fichier de log des requêtes (optionnel)
├── requirements.txt         # dépendances minimales pour l’API
├── README.md                # Guide rapide pour lancer et tester l'API
├── Dockerfile               # recette de construction de l’image Docker
├── .dockerignore            # fichiers à exclure du build (n'est pas vraiment utilisé dans cette démo)
└── journal_de_projet.md     # Suivi des décisions techniques
```

---

## 2. Lancer l’API **en local**

### 2.1. Installer les dépendances

Depuis la racine du projet (`Concrete/`) :

```bash
pip install -r requirements.txt
```

### 2.2. Lancer l’API

Toujours à la racine :

```bash
python -m app.main
```

> Important : on lance `python -m app.main` (et **pas** `python app/main.py`)
> car les imports sont du type `from app.charger_modele import ..., etc.`.

Si tout va bien, tu verras quelque chose comme :

```text
* Serving Flask app 'main'
* Running on http://127.0.0.1:8000
```

### 2.3. Tester l’API en local

Dans le navigateur :

* `http://127.0.0.1:8000/` → message d’accueil JSON


Pour un POST JSON, ouvrir un nouveau terminal et executer la ligne suivante en `curl` :

```bash
curl -X POST http://127.0.0.1:8000/predire \
     -H "Content-Type: application/json" \
     -d @donnees.json
```

---

## 3. Enregistrement des requêtes (log des requêtes)

Le fichier `app/utilites.py` contient une fonction :

```python
def log_request(payload, prediction) -> None:
    """
    Enregistre chaque requête + prédiction dans un fichier JSONL.
    Par défaut : requetes_enrg.jsonl
    """
```

Par défaut :

* le fichier de log est : `requetes_enrg.jsonl`
* chaque requête = **1 ligne JSON** (format JSONL)

Quand tu lances l’API **en local**, chaque appel à `/predire` ajoute une ligne dans `requetes_enrg.jsonl` dans le dossier du projet.

---

## 4. Construire l’image Docker (Ouvrir l'application Docker dans votre ordinateur)

### 4.1. Fichier `.dockerignore` (recommandé d'avoir ce fichier dans la racine du projet)

Exemple de `.dockerignore` :

```gitignore
venv/
.env/
*.env
__pycache__/
*.pyc
*.ipynb

mlruns/
.git/
.gitignore

data/
*.csv
*.parquet

*.log
```

### 4.2. Dockerfile (obligatoire d'avoir ce fichier dans la racine du projet)

Exemple de `Dockerfile` simple pour ce projet :

```dockerfile
FROM python:3.11-slim

# 1) Dossier de travail dans le conteneur
WORKDIR /app

# 2) Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copier le code de l'application
COPY app/ app/
COPY code/ code/
COPY test/ test/
COPY models/ models/
COPY journal_de_projet.md .
COPY requetes_enrg.jsonl .

# 4) (Optionnel) fichier de log initial
COPY requetes_enrg.jsonl requetes_enrg.jsonl

# 5) Ajouter /app au PYTHONPATH
ENV PYTHONPATH=/app

# 6) Exposer le port utilisé par Flask
EXPOSE 8000

# 7) Démarrer l'API
CMD ["python", "-m", "app.main"]
```

### 4.3. Construire l’image

Depuis la racine du projet :

```bash
docker build -t prediction-etudiante-api .
```

* `prediction-etudiante-api` = nom de l’image
* `.` = contexte de build (dossier courant)

---

## 5. Lancer l’API **dans Docker**

### 5.1. Lancer un conteneur simple

```bash
docker run -p 8000:8000 prediction-etudiante-api
```

* `-p 8000:8000` → connecte le port 8000 du conteneur au port 8000 de la machine
* l’API est accessible à `http://127.0.0.1:8000/`

Tester dans le navigateur :

* `http://127.0.0.1:8000/`

Tester `/predire` comme en local (curl, script Python, Thunder Client, etc.).

---

## 6. Enregistrer les requêtes **dans Docker** (et les voir sur la machine)

### 6.1. Lancer Docker avec un volume pour les logs

Pour que les requêtes soient enregistrées dans un fichier **sur la machine**, il faut utiliser un volume :

```bash
docker run -p 8000:8000 \
  -v "$(pwd)/requetes_enrg.jsonl:/app/requetes_enrg.jsonl" \
  prediction-etudiante-api
```

* `$(pwd)/requetes_enrg.jsonl` → fichier sur la machine
* `/app/requetes_enrg.jsonl` → fichier dans le conteneur
* les deux sont **synchronisés**.

Chaque requête à `/predire` ajoute une ligne dans `requetes_enrg.jsonl` **visible sur ta machine**.

### 6.2. Arrêter l’enregistrement des requêtes avec Docker

Plusieurs options :

1. **Arrêter le conteneur**
   → plus aucune requête n’est traitée → plus de logs.

2. Lancer un conteneur **sans volume** (sans `-v`)
   → les requêtes sont loggées dans le conteneur, mais pas sur ta machine.

3. **Désactiver log_request** dans le code (option pédagogique) :

   * commenter l’appel `log_request(...)` dans `app/main.py`
   * reconstruire l’image avec `docker build ...`

---

## 7. Voir ce qu’il y a **dans l’image / le conteneur**

### 7.1. Entrer dans un conteneur basé sur l’image

```bash
docker run -it --entrypoint /bin/sh prediction-etudiante-api
```

Puis, dans le shell du conteneur :

```sh
pwd         # devrait afficher /app
ls          # voir les fichiers copiés
ls app      # voir main.py, charger_modele.py, utilites.py
ls code     # voir modele_tree.pkl et features.pkl
cat requetes_enrg.jsonl   # voir le contenu du fichier de log (si présent)
```

Sortir du conteneur :

```sh
exit
```

### 7.2. Voir les conteneurs en cours d’exécution

```bash
docker ps
```

---

## 8. Arrêter proprement

### 8.1. Arrêter un conteneur qui tourne au premier plan

Si tu as lancé :

```bash
docker run -p 8000:8000 prediction-etudiante-api
```

→ pour arrêter : **Ctrl + C** dans ce terminal.

### 8.2. Arrêter un conteneur en arrière-plan

1. Voir les conteneurs :

   ```bash
   docker ps
   ```

2. Arrêter un conteneur :

   ```bash
   docker stop <CONTAINER_ID>
   ```

3. (Optionnel) Supprimer un conteneur arrêté :

   ```bash
   docker rm <CONTAINER_ID>
   ```

4. (Optionnel) Supprimer l’image :

   ```bash
   docker rmi prediction-etudiante-api
   ```

---

## 9 . Installer et initialiser Google Cloud SDK
- Installer l'application sur ordinateur windows : https://cloud.google.com/sdk/docs/install?hl=fr#windows
- Installer gcloud dans l'Environnement de l'API (si vous ne l'avez pas) c'est optionnel :
```bash
   pip install gcloud
```
- initialiser avec "gcloud init" dans powershell pour configurer rapidement le SDK Google Cloud lors de la première utilisation. Si vous voulez configurez votre compte et le projet manuellement sur la plateform Cloud ou dans le terminale, elle est donc optionnelle.

---

## 10. Déploiement sur Google Cloud
Sur la plateform de Google Cloud :
1. Aller dans Cloud Run
2. Ouvrir le sélecteur de projet
3. Cliquer sur "Nouveau projet" et créer un nouveau projet ex:(projetIApredictionetudiant)
3. Activer la facturation (même pour les quotas gratuits)
4. Activer les API nécessaires : Cloud Run, Artifact Registry.


# 10.1. Définir les variables
$PROJET_ID ="your-project-id"  # Remplacez par votre ID de projet GCP
$IMAGE_NAME_DOCKER="your-image-name"   # Remplacez par le nom de votre image Docker
$REGION="your-region"    # Remplacez 'your-region' par la région GCP de votre choix
$DEPOT_NAME="your-depot" # Remplacez 'your-depot' par le dépôt de Actifact Registry que vous utiliserez 


## Si vous devez installé le composant 'beta' s'il n'Est pas déjà installé (Optionnel)
```powershell
gcloud components install beta
```

## 10.2. Lier le projet au compte de facturation

```powershell
gcloud beta billing projects link ${PROJET_ID} `
   --billing-account={ID du compte de facturation}
```

gcloud beta billing projects link quiet-subset-479914-b9 `
  --billing-account=01D560-F214D7-332F87

## 10.3. Activer les services nécessaire
1. cloudbuild
2. artifactregistry

```powershell
gcloud services enable cloudbuild.googleapis.com artifactregistry.googleapis.com containerregistry.googleapis.com --project=${ID_PROJET}$
```

gcloud services enable cloudbuild.googleapis.com artifactregistry.googleapis.com containerregistry.googleapis.com --project=quiet-subset-479914-b9

---

## 11. Rôle IAM recommandés

## Donner les bons rôles à ton compte si vous ne disposez pas des autorisation requises
1. Service Usage Admin (roles/serviceusage.serviceUsageAdmin)
```
gcloud projects add-iam-policy-binding ${ID_PROJET} `
  --member="user:${YOUR_USER_ACCOUNT}" `
  --role="roles/serviceusage.serviceUsageAdmin"
```

gcloud projects add-iam-policy-binding quiet-subset-479914-b9 `
  --member="user:danielbourcierblake@gmail.com" `
  --role="roles/serviceusage.serviceUsageAdmin"

2. Cloud Build Editor
```
gcloud projects add-iam-policy-binding ${ID_PROJET} `
  --member="user:${YOUR_USER_ACCOUNT}$" `
  --role="roles/cloudbuild.builds.editor"
```

gcloud projects add-iam-policy-binding quiet-subset-479914-b9 `
  --member="user:danielbourcierblake@gmail.com" `
  --role="roles/cloudbuild.builds.editor"

---

## 11.1 Créer un dépot Docker
```Powershell
gcloud artifacts repositories create prediction-etudiante-repo `
  --repository-format=docker `
  --location=us-central1 `
  --description={"Écriver la fonction de votre dépot docker"} `
  --project=${PROJET_ID}
```

gcloud artifacts repositories create prediction-etudiante-repo `
  --repository-format=docker `
  --location=us-central1 `
  --description="Dépôt Docker pour l'API de prédiction étudiante" `
  --project=quiet-subset-479914-b9

## 12. Activer l'authentification Docker
```Powershell
   gcloud auth configure-docker
```
taper "y" et cliquer sur "Enter"

## 13. Construire et pousser l'image en format Docker
1. Construire localement l'image
```powershell
docker build -t us-central1-docker.pkg.dev/${ID_PROJET}/${DEPOT_NAME}/${IMAGE_NAME_DOCKER}:latest .
```

docker build -t us-central1-docker.pkg.dev/quiet-subset-479914-b9/prediction-etudiante-repo/prediction-etudiante-api:latest .

2. Tagger pour Artifact Registry 
```powershell
docker tag us-central1-docker.pkg.dev/quiet-subset-479914-b9/prediction-etudiante-api:latest us-central1-docker.pkg.dev/$PROJET_ID/$DEPOT_NAME/$IMAGE_NAME_DOCKER:latest
```
docker tag us-central1-docker.pkg.dev/quiet-subset-479914-b9/prediction-etudiante-api:latest us-central1-docker.pkg.dev/quiet-subset-479914-b9/prediction-etudiante-repo/prediction-etudiante-api:latest

3. Pousser l'image de Docker sur Google Cloud dans Artifact Registry
```powershell
docker push us-central1-docker.pkg.dev/$PROJET_ID/$DEPOT_NAME/$IMAGE_NAME_DOCKER:latest 
```

docker push us-central1-docker.pkg.dev/quiet-subset-479914-b9/prediction-etudiante-repo/prediction-etudiante-api:latest 
--- 
## En cas d'Erreur
Si la console affiche cette erreur :
" WARNING: [user@gmail.com] does not have permission to access projects instance [projetiapredictionetudiant] (or it may not exist): The caller does not have permission. This command is authenticated as user@gmail.com which is the active account specified by the [core/account] property
Are you sure you wish to set property [core/project] to projetiapredictionetudiant?

Do you want to continue (Y/n)? "

1. Tape "n" et "Enter"

2. Lister vos projets accessibles
```Powershell
   gcloud projects list
```

3. Sélecitonner le bon projet
```Powershell
   gcloud config set project ${ID_PROJET}
```
gcloud config set project quiet-subset-479914-b9

4. Activer Cloud Run sur ce projet

```Powershell
gcloud services enable run.googleapis.com --project=${ID_PROJET}
```
gcloud services enable run.googleapis.com --project=quiet-subset-479914-b9

---

# Déployment de l'image 

1. Effectuer le déployment de l'image sur Google Cloud Run
```Powershell

gcloud run deploy etudiant --image=us-central1-docker.pkg.dev/$PROJET_ID/$DEPOT_NAME/$IMAGE_NAME_DOCKER:latest --platform managed --region $REGION
```

gcloud run deploy etudiant --image=us-central1-docker.pkg.dev/quiet-subset-479914-b9/prediction-etudiante-repo/prediction-etudiante-api:latest --platform managed --region us-central1   

2. Autoriser les invocations non authentifiées pour accèder à ton service que tu a nommé

```Powershell
y + "Enter"
```
3. Si cela marche, alors le GCP génèrera un lien publique que vous pourriez utiliser pour obtenir des prédictions.


https://etudiant-xxxxxx.a.run.app/


4. Tester l'API sur le Cloud

```powershell
curl.exe -v -X POST "https://etudiant-xxxxxx-uc.a.run.app/predire" -H "Content-Type: application/json" --data-binary "@donnees.json"
```

curl.exe -v -X POST "https://etudiant-vjjhestyrq-uc.a.run.app/predire" -H "Content-Type: application/json" --data-binary "@donnees.json"
--- 

## 14 Erreurs

1. On a dû changer le port 8000 pour que le code Flask soit configuré sur le port 8080 pour pouvoir déployé l'API sur Google Cloud SDK
Il faut que tu change le port à 8080 sur le fichier "Main.py" et "Dockerfile" si ce n'est pas le cas 

2. Il fallait que la version scikit-learn soit à jour à 1.6.1 sur l'image.


