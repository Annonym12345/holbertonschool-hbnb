# 🔧 Guide de Dépannage - Problème de Connexion

## ❌ Problème: Le login ne fonctionne pas

### 📋 Diagnostic Étape par Étape

---

## ÉTAPE 1: Vérifier que l'API (Part 2) tourne

```bash
# Terminal 1 - Lancer Part 2
cd hbnb_part2
source venv/bin/activate
python run.py
```

**Vous devriez voir:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

**Si erreur "No module named 'flask'":**
```bash
pip install -r requirements.txt
```

---

## ÉTAPE 2: Tester l'API avec curl

```bash
# Test 1: Health check
curl http://localhost:5000/health

# Résultat attendu:
# {"status": "healthy"}

# Test 2: Créer un utilisateur
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@hbnb.com",
    "password": "Test123!",
    "first_name": "Test",
    "last_name": "User"
  }'

# Résultat: {"id": "...", "email": "test@hbnb.com", ...}

# Test 3: Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@hbnb.com",
    "password": "Test123!"
  }'

# Résultat: {"access_token": "eyJ0eXAi...", "user": {...}}
```

---

## ÉTAPE 3: Activer CORS dans Part 2

**CRITIQUE!** Sans CORS, le navigateur bloque les requêtes.

### Fichier: `hbnb_part2/app/api/v1/app.py`

```python
from flask import Flask
from flask_cors import CORS  # ← IMPORTER

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    # ⚠️ AJOUTER CES LIGNES ⚠️
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # ... reste du code
```

**Puis redémarrer Part 2:**
```bash
# Ctrl+C pour arrêter
python run.py
```

---

## ÉTAPE 4: Vérifier le Frontend

### Lancer Part 4:

```bash
# Terminal 2
cd hbnb_part4_final_complete
python3 -m http.server 8080
```

### Ouvrir dans le navigateur:

```
http://localhost:8080/test_api.html
```

### Tests à faire:

1. **Test 1: Health Check** → Doit être ✅
2. **Test 2: Créer Utilisateur** → Doit être ✅
3. **Test 3: Login** → Doit être ✅
4. **Test 4: Get Places** → Doit être ✅

---

## ÉTAPE 5: Tester la Page Login

### Ouvrir:
```
http://localhost:8080/login.html
```

### Ouvrir Console (F12):

**Onglet Console** - Vous devriez voir:
```
Scripts.js loaded successfully
Login.js loaded
DOM loaded for login page
```

**Onglet Network:**
- Activer "Preserve log"
- Entrer email/password
- Cliquer "Connexion"
- Regarder la requête POST vers `/auth/login`

---

## 🐛 Erreurs Courantes

### Erreur 1: "CORS policy: No 'Access-Control-Allow-Origin'"

**Cause:** CORS non activé dans Part 2

**Solution:**
```python
# Dans app/api/v1/app.py
from flask_cors import CORS
CORS(app)
```

---

### Erreur 2: "Failed to fetch"

**Cause:** Part 2 n'est pas lancé

**Solution:**
```bash
cd hbnb_part2
python run.py
```

---

### Erreur 3: "Invalid email or password"

**Cause:** Utilisateur n'existe pas

**Solution:**
```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@hbnb.com",
    "password": "Test123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

---

### Erreur 4: "validateEmail is not defined"

**Cause:** scripts.js pas chargé

**Solution:** Vérifier que login.html contient:
```html
<script src="scripts/scripts.js"></script>
<script src="scripts/login.js"></script>
```

---

## ✅ Checklist de Vérification

Avant de tester le login, vérifiez:

- [ ] MySQL tourne
- [ ] Base de données `hbnb_dev_db` existe
- [ ] Part 2 lancé sur port 5000
- [ ] CORS activé dans Part 2
- [ ] Health check fonctionne (`curl localhost:5000/health`)
- [ ] Utilisateur créé dans la base
- [ ] Part 4 lancé sur port 8080
- [ ] Console navigateur sans erreur
- [ ] scripts.js chargé (voir console)
- [ ] login.js chargé (voir console)

---

## 🧪 Test Complet de A à Z

```bash
# 1. Lancer MySQL
sudo service mysql start

# 2. Lancer Part 2
cd hbnb_part2
source venv/bin/activate
python run.py
# Garder ce terminal ouvert

# 3. Nouveau terminal - Créer utilisateur
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ismael@gmail.com",
    "password": "Ismael123!",
    "first_name": "Ismael",
    "last_name": "BSD"
  }'

# 4. Tester login via curl
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "ismael@gmail.com",
    "password": "Ismael123!"
  }'

# Si ça marche ici, ça marchera dans le navigateur!

# 5. Lancer Part 4
cd hbnb_part4_final_complete
python3 -m http.server 8080

# 6. Navigateur
# http://localhost:8080/login.html
# Email: ismael@gmail.com
# Password: Ismael123!
```

---

## 📞 Si Rien ne Marche

### Vérification MySQL:

```bash
mysql -u hbnb_dev -p
# Password: hbnb_dev_pwd

USE hbnb_dev_db;
SELECT * FROM users;
```

### Logs Python:

Ajouter dans `app/api/v1/app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Console Navigateur:

```javascript
// Tester manuellement dans Console (F12):
fetch('http://localhost:5000/api/v1/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        email: 'test@hbnb.com',
        password: 'Test123!'
    })
})
.then(r => r.json())
.then(d => console.log(d))
.catch(e => console.error(e));
```

---

## 🎯 Solution Rapide

Si vous voulez juste que ça marche MAINTENANT:

```bash
# 1. Part 2
cd hbnb_part2
source venv/bin/activate

# 2. Vérifier CORS
grep -n "CORS" app/api/v1/app.py
# Si pas trouvé, ajouter CORS comme indiqué ci-dessus

# 3. Lancer
python run.py

# 4. Nouveau terminal - Créer user
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"Test123!","first_name":"Test","last_name":"User"}'

# 5. Part 4
cd hbnb_part4_final_complete
python3 -m http.server 8080

# 6. Navigateur
# http://localhost:8080/login.html
# test@test.com / Test123!
```

**ÇA DEVRAIT MARCHER ! 🎉**
