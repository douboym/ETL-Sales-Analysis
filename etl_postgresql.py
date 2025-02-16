import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Text, Float, Integer, Date

# 🔹 1️⃣ Charger les données avec le bon encodage
file_path = "C:/Users/HP/OneDrive/.kaggle/data/sales_100k.csv"

try:
    df = pd.read_csv(file_path, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(file_path, encoding='latin1')

# 🔹 2️⃣ Supprimer les colonnes inutiles (ignorer si elles n'existent pas)
df.drop(columns=['Unnamed: 0', 'Sales_ID'], inplace=True, errors='ignore')

# 🔹 3️⃣ Nettoyer les valeurs manquantes
df = df.assign(
    Sales_Amount=df['Sales_Amount'].fillna(df['Sales_Amount'].mean()),
    Discount=df['Discount'].fillna(0),
    Customer_Age=df['Customer_Age'].fillna(df['Customer_Age'].median()),
    Customer_Gender=df['Customer_Gender'].fillna("Unknown")
)

# 🔹 4️⃣ Convertir Date_of_Sale en format date
df['Date_of_Sale'] = pd.to_datetime(df['Date_of_Sale'], errors='coerce')

# 🔹 5️⃣ Convertir Customer_Age en entier
df['Customer_Age'] = df['Customer_Age'].astype('Int64')  # Supporte les NaN

# 🔹 6️⃣ Vérifier et forcer l'encodage UTF-8 sur les colonnes textuelles
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].astype(str).apply(lambda x: x.encode('utf-8', errors='ignore').decode('utf-8'))

# 🔹 7️⃣ Connexion à PostgreSQL avec gestion des transactions
DB_USER = "postgres"  
DB_PASSWORD = "868011"  # 🔥 Remplace par ton mot de passe PostgreSQL
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ventes"

from sqlalchemy import create_engine, text

# 🔹 Connexion PostgreSQL avec autocommit activé
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', isolation_level="AUTOCOMMIT", echo=True)  # 🔹 Mode debug activé

with engine.connect() as connection:
    try:
        # 🔹 Supprimer la table avant d'insérer
        connection.execute(text("DROP TABLE IF EXISTS ventes_data;"))

        # 🔹 Insérer les données dans PostgreSQL
        df.to_sql('ventes_data', connection, if_exists='replace', index=False, dtype={
            "Product_Category": Text,
            "Sales_Amount": Float,
            "Discount": Float,
            "Sales_Region": Text,
            "Date_of_Sale": Date,
            "Customer_Age": Integer,
            "Customer_Gender": Text,
            "Sales_Representative": Text
        }, chunksize=5000)  # 🔹 Insertion par paquets de 5000 lignes

        print(f"\n✅ {len(df)} lignes insérées avec succès dans PostgreSQL !")

    except Exception as e:
        print("\n❌ Erreur lors de l'insertion :", e)
