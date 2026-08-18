import os
import requests
import pandas as pd
from dotenv import load_dotenv
import psycopg2

# 1. Charger les variables d'environnement depuis le fichier .env
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
# En local sur votre machine, on se connecte via localhost (le port 5432 est exposé)
# Dans Docker, le script se connectera via 'db'
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

def extract_data():
    """Étape 1: Extraction des données depuis une API publique"""
    print("Extraction des données depuis l'API...")
    # Exemple d'API publique : JSONPlaceholder (utilisateurs)
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"Extraction réussie : {len(data)} enregistrements récupérés.")
        return data
    else:
        raise Exception(f"Erreur lors de l'appel API : {response.status_code}")

def transform_data(raw_data):
    """Étape 2: Nettoyage et transformation des données avec Pandas"""
    print("Nettoyage et transformation des données...")
    
    # Conversion en DataFrame Pandas
    df = pd.DataFrame(raw_data)
    
    # Sélection et renommage des colonnes utiles
    df = df[['id', 'name', 'username', 'email', 'phone', 'website']]
    
    # Nettoyage : Mettre les e-mails en minuscules et supprimer les espaces superflus
    df['email'] = df['email'].str.lower().str.strip()
    df['name'] = df['name'].str.strip()
    
    # Ajout d'une colonne de métadonnée (très courant en Data Engineering)
    df['processed_at'] = pd.Timestamp.now()
    
    print("Transformation terminée.")
    return df

def load_data(df):
    """Étape 3: Chargement des données nettoyées dans PostgreSQL"""
    print("Chargement des données dans PostgreSQL...")
    
    try:
        # Connexion à la base de données
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        cursor = connection.cursor()
        
        # Création de la table si elle n'existe pas
        create_table_query = """
        CREATE TABLE IF NOT EXISTS public_users (
            id INT PRIMARY KEY,
            name VARCHAR(150),
            username VARCHAR(100),
            email VARCHAR(150),
            phone VARCHAR(100),
            website VARCHAR(150),
            processed_at TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        
        # Insertion des données ligne par ligne (ou par batch)
        for _, row in df.iterrows():
            insert_query = """
            INSERT INTO public_users (id, name, username, email, phone, website, processed_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                email = EXCLUDED.email,
                processed_at = EXCLUDED.processed_at;
            """
            cursor.execute(insert_query, (
                row['id'], row['name'], row['username'], 
                row['email'], row['phone'], row['website'], 
                row['processed_at']
            ))
            
        connection.commit()
        print(f"Chargement réussi : {len(df)} lignes insérées/mises à jour dans la base de données !")

    except Exception as error:
        print(f"Erreur lors de la connexion ou de l'insertion PostgreSQL : {error}")
    
    finally:
        if 'connection' in locals() and connection:
            cursor.close()
            connection.close()
            print("Connexion PostgreSQL fermée.")

if __name__ == "__main__":
    print("--- Début du pipeline ETL ---")
    raw = extract_data()
    cleaned_df = transform_data(raw)
    load_data(cleaned_df)
    print("--- Fin du pipeline ETL ---")
