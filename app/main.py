import pandas as pd
from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError

from app.charger_models import charger_modele

from app.utilites import log_request

modele = charger_modele()

app = Flask(__name__)


class DonneesEntree(BaseModel):
    age: float
    famsize: float
    Medu: float
    Fedu: float
    Mjob: float
    Fjob: float
    traveltime: float
    studytime: float
    failures: float
    famrel: float
    freetime: int
    goout: int
    Dalc: int
    Walc: int
    health: int
    absences: int
    G1: int
    G2: int
    school_GP: int
    school_MS: int
    romantic_no: int
    romantic_yes: int
    internet_no: int
    internet_yes: int
    nursery_no: int
    nursery_yes: int
    activities_no: int
    activities_yes: int
    higher_no: int
    higher_yes: int
    paid_no: int
    paid_yes: int
    famsup_no: int
    famsup_yes: int
    schoolsup_no: int
    schoolsup_yes: int
    Pstatus_A: int
    Pstatus_T: int
    sex_F: float
    sex_M: float
    address_R: float
    address_U: float
    reason_course: float
    reason_home: float
    reason_other: float
    reason_reputation: float
    guardian_father: float
    guardian_mother: float
    guardian_other: float


@app.route("/", methods=["GET"])
def accueil():
    """Message d'accueil pour vérifier que l'api fonctionne."""
    return jsonify({"message": "API de prédiction d'échec étudiant opérationnel"})


@app.route("/test", methods=["GET"])
def test():
    return "TEST OK"

RECALL_TEST = 80.5


@app.route("/predire", methods=["POST"])
def predire():
    """
    Reçoit un JSON, le valide, le prépare pour le modèle,
    effectue la prédiction, enregistre la requête,
    puis retourne le résultat.
    """

    # S’assurer qu’un JSON a été envoyé
    if not request.json:
        return jsonify({"erreur": "Aucun JSON fourni"}), 400

    try:
        # 1) Valider les données avec Pydantic
        donnees = DonneesEntree(**request.json)

        # 2) Transformer en DataFrame (format attendu par le modèle)
        donnees_df = pd.DataFrame([donnees.model_dump()])

        # 2.b) Adapter les noms de colonnes à ceux utilisés pour entraîner le modèle
        donnees_df = donnees_df.rename(columns={
            "famsize": "Taille de la famille",
            "school_GP": "school GP",
            "school_MS": "school MS",
            "romantic_no": "romantic no",
            "romantic_yes": "romantic yes",
            "internet_no": "internet no",
            "internet_yes": "internet yes",
            "nursery_no": "nursery no",
            "nursery_yes": "nursery yes",
            "activities_no": "activities no",
            "activities_yes": "activities yes",
            "higher_no": "higher no",
            "higher_yes": "higher_yes",
            "paid_no": "paid no",
            "paid_yes": "paid yes",
            "famsup_no": "famsup no",
            "famsup_yes": "famsup yes",
            "schoolsup_no": "schoolsup no",
            "schoolsup_yes": "schoolsup yes",
            "Pstatus_A": "Pstatus A",
            "Pstatus_T": "Pstatus T",
            "sex_F": "sex F",
            "sex_M": "sex M",
            "address_R": "address R",
            "address_U": "address U",
            "reason_course": "reason course",
            "reason_home": "reason home",
            "reason_other": "reason other",
            "reason_reputation": "reason reputation",
            "guardian_father": "guardian father",
            "guardian_mother": "guardian mother",
            "guardian_other": "guardian other"
        })

        # 3) Faire la prédiction
        prediction = float(modele.predict(donnees_df)[0])
        
        # 3.b) Construire un intervalle de confiance SIMPLE
        borne_inferieure = prediction - RECALL_TEST
        borne_superieure = prediction + RECALL_TEST

        # Optionnel : éviter les valeurs négatives si ça n'a pas de sens
        borne_inferieure = max(0.0, borne_inferieure)

        # 4) Préparer la réponse
        resultat = donnees.model_dump()
        resultat["prediction_resistance"] = prediction
        resultat["intervalle_confiance_min"] = borne_inferieure
        resultat["intervalle_confiance_max"] = borne_superieure

        # 5) Enregistrer la requête dans un fichier JSONL pour analyse
        log_request(donnees.model_dump(), prediction)

        # 6) Retourner la réponse à l’utilisateur
        return jsonify({"resultats": resultat})

    except ValidationError as ve:
        # Erreurs provenant de Pydantic (données manquantes ou mal formatées)
        return jsonify({"erreur": ve.errors()}), 400

    except Exception as e:
        # Autres erreurs inattendues (ex : modèle mal chargé)
        return jsonify({"erreur": str(e)}), 500


#---------------------------------
# 5) Lancer l'Application Flask
#----------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)