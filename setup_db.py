import MySQLdb

# Database credentials
DB_HOST = "127.0.0.1"
DB_USER = "root"  # Change if needed
DB_PASSWORD = "Aditya@9476"  # Change to your MySQL password
TEST_DB_NAME = "test_kbc_game"

# Table creation queries
TABLES = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            uid VARCHAR(255) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            dob DATE NOT NULL,
            qualification VARCHAR(100) NOT NULL,
            status ENUM('waiting', 'accepted', 'rejected') NOT NULL DEFAULT 'waiting'
        );
    """,
}

def setup_database():
    try:
        # Connect to MySQL Server
        connection = MySQLdb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=TEST_DB_NAME)
        cursor = connection.cursor()
        
        # Create test database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {TEST_DB_NAME};")
        cursor.execute(f"USE {TEST_DB_NAME};")
        
        # Create required tables
        for table_name, table_query in TABLES.items():
            cursor.execute(table_query)
        
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Test database '{TEST_DB_NAME}' has been set up successfully!")
    
    except MySQLdb.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    setup_database()
