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
- Installer gcloud (si vous ne l'avez pas):
```bash
   pip install gcloud
```
- initialiser avec gcloud init

---

## 10. Déploiement sur Google Cloud
Sur la plateform de Google Cloud :
1. Aller dans Cloud Run
2. Ouvrir le sélecteur de projet
3. Cliquer sur "Nouveau projet" et créer un nouveau projet ex:(projetIApredictionetudiant)
3. Activer la facturation (même pour les quotas gratuits)
4. Activer les API nécessaires : Cloud Run, Artifact Registry.

Dans le terminale :
1. taguer l'image pour qu'elle soit prête à être pousser dans Artifact Registry;
   ```bash
   docker tag prediction-etudiante-api gcr.io/projetiapredictionetudiant/prediction-etudiante-api
   ```
2. Pousser l'image sur le Google Cloud
   ```bash
   docker push gcr.io/projetiapredictionetudiant/prediction-etudiante-api
   ```
---
