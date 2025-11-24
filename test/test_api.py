import requests

URL = "http://127.0.0.1:8000/predire"

donnees_predire = {
    "age": 27,
    "famsize": "GT3",
    "Medu": 1,
    "Fedu": 2,
    "Mjob": "at_home",
    "Fjob": "other",
    "traveltime": 2,
    "studytime": 1,
    "failures": 3,
    "famrel": 3,
    "freetime": 5,
    "goout": 5,
    "Dalc": 4,
    "Walc": 4,
    "health": 2,
    "absences": 3,
    "G1": 0,
    "G2": 0,
    "school": "GP",
    "romantic": "yes",
    "internet": "no",
    "nursery": "yes",
    "activities": "no",
    "higher": "no",
    "paid": "yes",
    "famsup": "no",
    "schoolsup": "no",
    "Pstatus": "A",
    "sex": "M",
    "address": "R",
    "reason": "other",
    "guardian": "mother"
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