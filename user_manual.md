1. Entrer l'adresse de l'API situé sur Google Cloud sur une page web.
Enter :
"https://etudiant-vjjhestyrq-uc.a.run.app"


2. Si un message apparait cela signifie que vous êtes connectés à l'API sur Google Cloud

3. Créer un fichier .json qui remplit les caractèristiques que l'API doit lire pour effectué la prédiction 

4. Dans un terminale effectuer une requête de prédiction pour savoir si l'étudiant va échouer ou réussir.

```powershell
curl.exe -v -X POST "https://etudiant-vjjhestyrq-uc.a.run.app/predire" -H "Content-Type: application/json" --data-binary "@donnees.json"
```
