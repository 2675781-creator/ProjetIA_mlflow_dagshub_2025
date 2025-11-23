import requests

URL = "http://127.0.0.1:8000/predire"

donnees_predire = {
    "age": 27,
    "famsize": 1,
    "Medu": None,
    "Fedu": 4,
    "Mjob": 0.831633,
    "Fjob": None,
    "traveltime": 2,
    "studytime": 3,
    "failures": 0,
    "famrel": 3,
    "freetime": 2,
    "goout": 4,
    "Dalc": 1,
    "Walc": 1,
    "health": 5,
    "absences": 0,
    "G1": 15,
    "G2": 10,
    "school_GP": 0,
    "school_MS": 1,
    "romantic_no": 1,
    "romantic_yes": 0,
    "internet_no": 0,
    "internet_yes": 1,
    "nursery_no": 1,
    "nursery_yes": 0,
    "activities_no": 0,
    "activities_yes": 1,
    "higher_no": 0,
    "higher_yes": 1,
    "paid_no": 0,
    "paid_yes": 1,
    "famsup_no": 1,
    "famsup_yes": 0,
    "schoolsup_no": 0,
    "schoolsup_yes": 1,
    "Pstatus_A": 1,
    "Pstatus_T": 0,
    "sex_F": 0,
    "sex_M": 1,
    "address_R": 1,
    "address_U": 0,
    "reason_course": 0,
    "reason_home": 0,
    "reason_other": 1,
    "reason_reputation": 0,
    "guardian_father": 1,
    "guardian_mother": 1,
    "guardian_other": 0
}

if __name__ == "__main__":
    try:
        response = requests.post(URL, json=donnees_predire)

        print("Status code :", response.status_code)

        try:
             # Essaie d'afficher la réponse au format JSON
            print("Réponse JSON :")
            print(response.json())
        except Exception:
            # Si la réponse n'est pas du JSON, l'affiche telle quelle
            print("Réponse brute :")
            print(response.text)

    except Exception as e:
        # Si le serveur est éteint / inaccessible
        print("Erreur lors de l'appel à l'API :", e)