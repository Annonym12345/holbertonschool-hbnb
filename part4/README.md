# 🚀 HBnB Evolution - Guide d'Installation COMPLET
## Parts 2, 3 et 4 - De A à Z

---

## 📦 Ce que vous avez

### Part 2 - Backend API (SQLAlchemy + Flask)
- ✅ Modèles SQLAlchemy complets
- ✅ Repository Pattern
- ✅ Business Logic (Facade)
- ✅ API REST complète
- ✅ JWT Authentication
- ✅ MySQL database

### Part 3 - Frontend Flask (Templates)
- ✅ Templates Jinja2
- ✅ Page login avec cadenas
- ✅ Session management
- ✅ Integration API

### Part 4 - Simple Web Client (HTML/CSS/JS)
- ✅ Pure JavaScript SPA
- ✅ 4 pages HTML
- ✅ CSS complet
- ✅ 5 fichiers JavaScript
- ✅ Images SVG
- ✅ 100% Holberton compliant

---

## 🎯 Installation Complète - Étape par Étape

### ÉTAPE 1: Préparer l'environnement

```bash
# 1. Créer un dossier de travail
mkdir holbertonschool-hbnb
cd holbertonschool-hbnb

# 2. Extraire les 3 parties
tar -xzf hbnb_part2_complete.tar.gz
tar -xzf hbnb_part3_complete.tar.gz
tar -xzf hbnb_part4_complete.tar.gz

# Structure finale:
# holbertonschool-hbnb/
# ├── hbnb_part2/    (API Backend)
# ├── hbnb_part3/    (Frontend Flask)
# └── hbnb_part4/    (Web Client)
```

---

### ÉTAPE 2: Setup MySQL Database

```bash
# 1. Lancer MySQL
mysql -u root -p

# 2. Exécuter le script de setup
mysql -u root -p < hbnb_part2/setup_db.sql

# Cela créera:
# - Base de données: hbnb_dev_db
# - Utilisateur: hbnb_dev / hbnb_dev_pwd
# - Base de test: hbnb_test_db
```

---

### ÉTAPE 3: Part 2 - Backend API

```bash
cd hbnb_part2

# 1. Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 2. Installer dépendances
pip install -r requirements.txt

# 3. Configurer .env
cp .env.example .env
# Éditer .env si nécessaire

# 4. Lancer l'API
python run.py

# ✅ API tourne sur http://localhost:5000
```

**Tester l'API:**
```bash
# Dans un autre terminal
curl http://localhost:5000/health
# Devrait retourner: {"status": "healthy"}
```

---

### ÉTAPE 4: Part 3 - Frontend Flask (OPTIONNEL)

```bash
# Ouvrir un nouveau terminal
cd holbertonschool-hbnb/hbnb_part3

# 1. Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 2. Installer dépendances
pip install -r requirements.txt

# 3. Configurer .env
cp .env.example .env

# 4. Lancer l'application
python run.py

# ✅ Frontend tourne sur http://localhost:8000
```

**Tester:**
```
Ouvrir navigateur: http://localhost:8000/login
```

---

### ÉTAPE 5: Part 4 - Web Client (RECOMMANDÉ)

```bash
# Ouvrir un nouveau terminal
cd holbertonschool-hbnb/hbnb_part4

# Lancer serveur web
python3 -m http.server 8080

# ✅ Web client tourne sur http://localhost:8080
```

**Tester:**
```
Ouvrir navigateur: http://localhost:8080/login.html
```

---

## 🔧 Configuration CORS (IMPORTANT!)

Pour que Part 4 fonctionne avec Part 2, vous DEVEZ activer CORS.

### Dans Part 2: `hbnb_part2/app/api/v1/app.py`

**Ajouter après la ligne `app = Flask(__name__)`:**

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ← AJOUTER CETTE LIGNE

# ... reste du code
```

**OU configuration spécifique:**

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:8080",
            "http://localhost:8000"
        ]
    }
})
```

**Puis redémarrer Part 2:**
```bash
# Arrêter (Ctrl+C) et relancer
python run.py
```

---

## 📊 Résumé des Ports

| Service | Port | URL | Commande |
|---------|------|-----|----------|
| **Part 2 - API** | 5000 | http://localhost:5000 | `python run.py` |
| **Part 3 - Flask** | 8000 | http://localhost:8000 | `python run.py` |
| **Part 4 - Web** | 8080 | http://localhost:8080 | `python3 -m http.server 8080` |

---

## 🧪 Test Complet du Système

### Test 1: API Backend (Part 2)

```bash
# Terminal 1: Lancer Part 2
cd hbnb_part2
source venv/bin/activate
python run.py

# Terminal 2: Tester
curl http://localhost:5000/health
curl http://localhost:5000/api/v1/countries
```

### Test 2: Web Client (Part 4)

```bash
# Terminal 1: Part 2 doit tourner (port 5000)
# Terminal 2: Lancer Part 4
cd hbnb_part4
python3 -m http.server 8080
```

**Dans le navigateur:**

1. **Aller sur:** http://localhost:8080/login.html
2. **Créer un utilisateur** (via API ou directement)
3. **Se connecter**
4. **Vérifier:**
   - ✅ Redirect vers index.html
   - ✅ Places s'affichent
   - ✅ Filtres fonctionnent
   - ✅ Clic "View Details" → place.html
   - ✅ Reviews s'affichent
   - ✅ Formulaire review visible (si connecté)

---

## 🗄️ Données de Test

### Créer un utilisateur admin via API:

```bash
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hbnb.com",
    "password": "Admin123!",
    "first_name": "Admin",
    "last_name": "User"
  }'
```

### Se connecter:

```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hbnb.com",
    "password": "Admin123!"
  }'
```

Cela retourne un token JWT.

### Ou utiliser les données SQL:

```bash
# Si vous voulez des données de test
cd hbnb_part3
mysql -u hbnb_dev -p hbnb_dev_db < sql_scripts/01_sample_data.sql
```

---

## 🎨 Screenshots - Ce que vous devriez voir

### Page Login (http://localhost:8080/login.html)
```
┌─────────────────────────────────┐
│         🔒 (Lock Icon)          │
│       Welcome Back              │
│   Sign in to continue to HBnB   │
│                                 │
│  📧 Email Address               │
│  [___________________]          │
│                                 │
│  🔑 Password          👁️       │
│  [___________________]          │
│                                 │
│  [   Sign In   ]                │
│                                 │
│  Don't have account? Sign up    │
│  ← Back to Home                 │
└─────────────────────────────────┘
```

### Page Index (http://localhost:8080/index.html)
```
┌────────────────────────────────────────┐
│  🏠 HBnB          Home    [Login]      │
├────────────────────────────────────────┤
│  Find Your Perfect Place               │
│  Filter by Price: [All ▼]              │
├────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐            │
│  │  [Image] │  │  [Image] │            │
│  │  Paris   │  │  London  │            │
│  │  $120/nt │  │  $150/nt │            │
│  │[Details] │  │[Details] │            │
│  └──────────┘  └──────────┘            │
└────────────────────────────────────────┘
```

---

## ⚠️ Problèmes Courants et Solutions

### Problème 1: "Connection refused" sur port 5000

**Solution:**
```bash
# Vérifier si Part 2 tourne
ps aux | grep python

# Si non, lancer Part 2
cd hbnb_part2
source venv/bin/activate
python run.py
```

### Problème 2: CORS Error dans la console

**Solution:**
```python
# Dans hbnb_part2/app/api/v1/app.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # AJOUTER CETTE LIGNE
```

### Problème 3: Places ne s'affichent pas

**Solutions:**
1. Vérifier que l'API retourne des données:
   ```bash
   curl http://localhost:5000/api/v1/places
   ```

2. Ouvrir la console du navigateur (F12)
3. Vérifier l'onglet Network
4. Chercher les erreurs JavaScript

### Problème 4: Login ne fonctionne pas

**Solutions:**
1. Vérifier que l'utilisateur existe:
   ```bash
   mysql -u hbnb_dev -p hbnb_dev_db
   SELECT * FROM users;
   ```

2. Créer un utilisateur via API
3. Vérifier les credentials
4. Vérifier la console navigateur

### Problème 5: Images ne s'affichent pas

**Solution:**
Les images SVG sont déjà créées dans `hbnb_part4/images/`
- logo.svg
- icon.svg
- placeholder.svg

---

## 📂 Structure Finale Complète

```
holbertonschool-hbnb/
│
├── hbnb_part2/                    # BACKEND API
│   ├── app/
│   │   ├── models/               # SQLAlchemy models
│   │   ├── persistence/          # Repository
│   │   ├── services/             # Facade
│   │   └── api/                  # Flask API
│   ├── tests/
│   ├── config.py
│   ├── requirements.txt
│   └── run.py                    # Port 5000
│
├── hbnb_part3/                    # FRONTEND FLASK
│   ├── app/
│   │   ├── templates/            # Jinja2 templates
│   │   └── static/               # CSS, JS
│   ├── config.py
│   ├── requirements.txt
│   └── run.py                    # Port 8000
│
└── hbnb_part4/                    # WEB CLIENT
    ├── index.html
    ├── login.html
    ├── place.html
    ├── add_review.html
    ├── styles/
    │   └── styles.css
    ├── scripts/
    │   ├── scripts.js
    │   ├── login.js
    │   ├── index.js
    │   ├── place.js
    │   └── add_review.js
    ├── images/
    │   ├── logo.svg              # ✅ Créé
    │   ├── icon.svg              # ✅ Créé
    │   └── placeholder.svg       # ✅ Créé
    └── README.md
```

---

## ✅ Checklist de Validation

### Part 2 - Backend
- [ ] MySQL configuré
- [ ] Base de données créée
- [ ] Dépendances installées
- [ ] API tourne sur port 5000
- [ ] Endpoint /health retourne 200
- [ ] CORS activé

### Part 3 - Frontend Flask (optionnel)
- [ ] Dépendances installées
- [ ] API_BASE_URL configuré
- [ ] Application tourne sur port 8000

### Part 4 - Web Client
- [ ] Serveur web lancé sur port 8080
- [ ] Toutes les pages accessibles
- [ ] Login fonctionne
- [ ] Places s'affichent
- [ ] Filtres fonctionnent
- [ ] Reviews visibles
- [ ] Formulaire review fonctionne

---

## 🎯 Pour 100% Holberton

### Validation HTML (W3C)
```bash
# Aller sur https://validator.w3.org/
# Valider chaque page:
- index.html
- login.html
- place.html
- add_review.html
```

### Validation CSS
```bash
# Aller sur https://jigsaw.w3.org/css-validator/
# Valider: styles/styles.css
```

### Tests JavaScript
```bash
# Ouvrir console navigateur (F12)
# Vérifier: aucune erreur JavaScript
```

---

## 🚀 Commandes Rapides

### Démarrage Complet

**Terminal 1 - Backend:**
```bash
cd hbnb_part2
source venv/bin/activate
python run.py
```

**Terminal 2 - Web Client:**
```bash
cd hbnb_part4
python3 -m http.server 8080
```

**Navigateur:**
```
http://localhost:8080/login.html
```

---

## 📞 Support

Si problème, vérifier:
1. Part 2 (API) tourne bien sur port 5000
2. CORS activé dans Part 2
3. MySQL database créée et accessible
4. Aucune erreur dans console navigateur (F12)

---

**🎉 Vous avez maintenant un système complet et fonctionnel ! 🎉**

**Bon courage avec Holberton ! 🚀**
