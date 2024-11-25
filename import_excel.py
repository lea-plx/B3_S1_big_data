import os
import pandas as pd
from sqlalchemy import create_engine

# Configuration de la base de données
DB_USER = 'root'        # Nom d'utilisateur de la base de données
DB_PASSWORD = 'root'  # Mot de passe de la base de données
DB_HOST = 'localhost'   # Remplacez par le nom du service Docker si nécessaire
DB_PORT = '3306'        # Port de la base de données
DB_NAME = 'crypto_top_15'   # Nom de votre base de données

# Créer une connexion à la base de données
engine = create_engine(f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Répertoire contenant les fichiers Excel
EXCEL_DIR = './excel_files'

def extract_crypto_name(file_name):
    """Extrait le nom de la crypto à partir du début du nom du fichier."""
    return file_name.split('_')[0]

def import_csv_to_db(file_path, table_name):
    """Importe un fichier CSV dans une table SQL en modifiant les données."""
    try:
        # Lire le fichier CSV en spécifiant le séparateur comme un point-virgule
        df = pd.read_csv(file_path, sep=';')
        
        # Supprimer les deux premières colonnes (ou les colonnes spécifiques si connues)
        df = df.drop(['timeHigh', 'timeLow'], axis=1, errors='ignore')  # Ajout de 'errors="ignore"' pour éviter une erreur si les colonnes n'existent pas
        
        # Ajouter une nouvelle colonne avec le nom de la crypto
        crypto_name = extract_crypto_name(os.path.basename(file_path))
        df['crypto_name'] = crypto_name
        
        # Afficher un aperçu des données avant l'insertion
        print(df.head())

        # Importer les données dans la base de données
        df.to_sql(table_name, con=engine, if_exists='append', index=False)

        print(f"Nom de la crypto extrait : {crypto_name}")
        
        print(f"✅ Fichier '{file_path}' importé avec succès dans '{table_name}'.")
    except Exception as e:
        print(f"❌ Erreur lors de l'importation de '{file_path}': {e}")
        
def main():
    # Lister tous les fichiers CSV dans le répertoire
    for file in os.listdir(EXCEL_DIR):  # Remplacer EXCEL_DIR par le répertoire des CSV
        if file.endswith('.csv'):
            print(f"Fichier trouvé : {file}")  # Ajoute cette ligne pour vérifier les fichiers trouvés
            file_path = os.path.join(EXCEL_DIR, file)
            table_name = 'crypto_data'  # Nom de la table cible
            
            # Importer le fichier CSV dans la base de données
            import_csv_to_db(file_path, table_name)

if __name__ == "__main__":
    main()