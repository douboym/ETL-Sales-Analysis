# 📊 Pipeline ETL - Analyse des Ventes avec API Kaggle, PostgreSQL & Power BI

## 🚀 Introduction
Ce projet met en place un **pipeline ETL automatisé** permettant d'extraire, transformer et charger des données de ventes issues de **l'API Kaggle** dans une base **PostgreSQL**, puis d'analyser ces données à l'aide de **Power BI**.

## 🛠 Technologies utilisées
- **Python** : Pandas, Requests, SQLAlchemy
- **API Kaggle** : Extraction automatisée des données
- **PostgreSQL** : Stockage des données et requêtes SQL
- **Power BI** : Visualisation et analyse des ventes

---

## ⚙️ Architecture du pipeline ETL
📍 **Étapes du pipeline :**
1️⃣ **Extraction** : Récupération des données via **l’API Kaggle**
2️⃣ **Transformation** : Nettoyage des valeurs manquantes, encodage et typage des données
3️⃣ **Chargement** : Stockage optimisé dans **PostgreSQL** via `\copy`
4️⃣ **Visualisation** : Connexion à **Power BI** pour l'analyse interactive

![ETL Architecture](https://raw.githubusercontent.com/your-repo-path/etl_pipeline_architecture.png)

---

## 🔹 Étape 1 : Extraction des données via l'API Kaggle
Nous utilisons l'API Kaggle pour récupérer les données du dataset **Retail Sales Data**.

### 📌 Installation et configuration de Kaggle API
1. **Créer une clé API Kaggle** :
   - Se rendre sur [Kaggle](https://www.kaggle.com/), aller dans **Account Settings** et télécharger `kaggle.json`.
   - Placer `kaggle.json` dans le dossier `~/.kaggle/` (ou `%USERPROFILE%/.kaggle/` sous Windows).

2. **Installer la bibliothèque Kaggle** :
```bash
pip install kaggle
```

3. **Télécharger les données depuis l'API** :
```python
import kaggle

# Télécharger les données Kaggle
dataset = "noir1112/retail-sales-data"
kaggle.api.dataset_download_files(dataset, path="data/", unzip=True)
print("✅ Données téléchargées avec succès !")
```

---

## 🔹 Étape 2 : Transformation et nettoyage des données avec Pandas
Nous utilisons **Pandas** pour :
- **Supprimer les colonnes inutiles**
- **Gérer les valeurs manquantes**
- **Convertir les formats des données**

```python
import pandas as pd

# Charger les données
file_path = "data/sales_100k.csv"
df = pd.read_csv(file_path, encoding='utf-8')

# Nettoyage des données
df.drop(columns=['Unnamed: 0', 'Sales_ID'], inplace=True, errors='ignore')
df.fillna({
    'Sales_Amount': df['Sales_Amount'].mean(),
    'Discount': 0,
    'Customer_Age': df['Customer_Age'].median(),
    'Customer_Gender': "Unknown"
}, inplace=True)

# Conversion des types
df['Date_of_Sale'] = pd.to_datetime(df['Date_of_Sale'], errors='coerce')
df['Customer_Age'] = df['Customer_Age'].astype('Int64')

# Sauvegarder en CSV pour PostgreSQL
file_path_cleaned = "data/ventes_clean.csv"
df.to_csv(file_path_cleaned, index=False, encoding='utf-8')
print("✅ Données nettoyées et sauvegardées !")
```

---

## 🔹 Étape 3 : Chargement des données dans PostgreSQL
Nous utilisons PostgreSQL pour **stocker les données proprement et optimiser les requêtes**.

### 📌 Création de la base et de la table
Dans **pgAdmin** ou **psql**, exécuter :
```sql
CREATE DATABASE ventes;
\c ventes;

CREATE TABLE ventes_data (
    Product_Category TEXT,
    Sales_Amount FLOAT,
    Discount FLOAT,
    Sales_Region TEXT,
    Date_of_Sale DATE,
    Customer_Age INTEGER,
    Customer_Gender TEXT,
    Sales_Representative TEXT
);
```

### 📌 Importer les données dans PostgreSQL avec `\copy`
Dans **psql**, exécuter :
```sql
\copy ventes_data FROM 'data/ventes_clean.csv' WITH CSV HEADER ENCODING 'UTF8';
SELECT COUNT(*) FROM ventes_data;
```
✅ **Les données sont maintenant chargées dans PostgreSQL !**

---

## 🔹 Étape 4 : Connexion et visualisation dans Power BI
### 📌 Connexion PostgreSQL → Power BI
1. **Ouvrir Power BI**
2. **Aller dans "Obtenir des données" → "Base de données PostgreSQL"**
3. **Entrer les informations :**
   - **Serveur** : `localhost`
   - **Base de données** : `ventes`
   - **Authentification** : `postgres` / `ton_mot_de_passe`
4. **Sélectionner la table `ventes_data` et charger les données**

### 📌 Création d'un premier dashboard
1. **Ajouter un graphique en barres**
2. **Mettre "Sales_Region" en axe X et "Sales_Amount" en axe Y**
3. **Ajouter des filtres interactifs pour explorer les données**

✅ **Tu as maintenant un dashboard interactif connecté à PostgreSQL !** 🎉

---

## 📊 Résultats et insights
### **🔍 Analyse des ventes par région :**
```sql
SELECT Sales_Region, COUNT(*) AS nb_ventes, SUM(Sales_Amount) AS total_ventes
FROM ventes_data
GROUP BY Sales_Region
ORDER BY total_ventes DESC;
```
📌 **Ce type d’analyse permet d'identifier les meilleures performances commerciales par région.**

---

## 📌 Comment exécuter ce projet ?
### 1️⃣ Installer les dépendances
```bash
pip install pandas kaggle sqlalchemy psycopg2
```
### 2️⃣ Exécuter le pipeline
```bash
python etl_postgresql.py
```
### 3️⃣ Vérifier les données dans PostgreSQL
```sql
SELECT COUNT(*) FROM ventes_data;
```
### 4️⃣ Ouvrir Power BI et se connecter à PostgreSQL

---

## 🎯 Conclusion
Ce projet montre comment **automatiser un pipeline ETL** depuis **l’API Kaggle** jusqu’à **Power BI**, en passant par **PostgreSQL**. 🎯

📢 **Améliorations possibles :**
- Automatiser l'exécution avec **Airflow**
- Ajouter une API Flask pour interroger les données
- Déployer un dashboard web interactif

🚀 **N’hésitez pas à contribuer ou poser des questions !*

