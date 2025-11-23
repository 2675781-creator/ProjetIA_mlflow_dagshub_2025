from functools import lru_cache
from pathlib import Path
import joblib

MODEL_SOURCE = "local"

MODEL_LOCAL_PATH = Path("models/modele_tree.pkl")


def _load_local_model():
    """Chargement d'un modèle local enregistré au format .pkl"""
    if not MODEL_LOCAL_PATH.exists():
        raise FileNotFoundError(f"Modèle local introuvable : {MODEL_LOCAL_PATH.resolve()}")
    return joblib.load(MODEL_LOCAL_PATH)


@lru_cache
def charger_modele():
    if MODEL_SOURCE == "local":
        return _load_local_model()
    
    else:
        raise ValueError("MODEL_SOURCE doit être 'local'.")