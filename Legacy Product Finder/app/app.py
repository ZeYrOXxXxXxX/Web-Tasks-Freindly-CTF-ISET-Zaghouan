import os
import mysql.connector
from flask import Flask, request, render_template

app = Flask(__name__)

def db_connect():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database=os.environ.get('DB_NAME')
    )

@app.route('/', methods=['GET'])
def index():
    product_id = request.args.get('id', '1')
    db_error = None
    product = None
    
    try:
        conn = db_connect()
        cursor = conn.cursor()
        
        # --- VULNÉRABILITÉ ---
        # L'ID est directement concaténé dans la requête.
        query = "SELECT name, description FROM products WHERE id = '" + product_id + "'"
        cursor.execute(query)
        product = cursor.fetchone()
        
    except mysql.connector.Error as err:
        # Les erreurs de la BDD sont affichées directement à l'utilisateur.
        db_error = f"Database Error: {err}"
        
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            
    return render_template('index.html', product=product, error=db_error, product_id=product_id)