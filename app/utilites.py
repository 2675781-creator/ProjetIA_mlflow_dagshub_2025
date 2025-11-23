import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

LOG_FILE = Path("requetes_enrg.jsonl")


def log_request(donnees_predire: Dict[str, Any], prediction: Any) -> None:
    """
    Enregistre chaque requête utilisateur + prédiction dans un fichier JSONL.

    - donnees_predire : données envoyées par l’utilisateur
    - prediction : résultat du modèle pour cette requête

    Format JSONL : 1 requête = 1 ligne JSON.
    C’est pratique pour l'analyse, car chaque ligne représente un enregistrement indépendant.
    """

    # Création d’un enregistrement (ligne JSON) avec timestamp, données d'entrée et prédiction
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),  # Horodatage précis en UTC
        "donnees_predire": donnees_predire,                                   # Données envoyées
        "prediction": prediction,                             # Résultat du modèle
    }

    # Crée le dossier s’il n'existe pas (utile si plus tard tu mets un chemin du type logs/requetes.jsonl)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # On ouvre le fichier en mode "append" pour ajouter une ligne (JSONL = JSON par ligne)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        # ensure_ascii=False permet de garder les accents visibles (é, è, à…)
