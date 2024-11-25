import pymysql

# Configuration de la base de données
DB_HOST = 'localhost'       # Remplacez par l'adresse ou le nom de votre conteneur si Docker est utilisé
DB_PORT = 3306              # Port MySQL
DB_USER = 'root'            # Nom d'utilisateur
DB_PASSWORD = 'root'    # Mot de passe (changez selon votre config)
DB_NAME = 'crypto_top_15'   # Nom de votre base de données

def test_connection():
    """Se connecte à la base de données et exécute une requête SELECT."""
    try:
        # Établir la connexion
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("✅ Connexion réussie à la base de données.")
        
        # Exécuter une requête SELECT
        with connection.cursor() as cursor:
            query = "SELECT * FROM NewTable;"  # Requête SQL simple
            cursor.execute(query)
            
            # Afficher les résultats
            results = cursor.fetchall()
            print("Résultats de la table NewTable :")
            for row in results:
                print(row)
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        # Fermer la connexion
        connection.close()

if __name__ == "__main__":
    test_connection()