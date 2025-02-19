from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
import os
from datetime import datetime

app = Flask(__name__)


DATABASE_URL = os.getenv('DATABASE_URL', 'dbname=mydb user=postgres password=password1 host=localhost port=5432')

def init_db():
    """Database initialization."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS media_urls (
            url TEXT PRIMARY KEY,
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            downloaded INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/add_urls', methods=['GET', 'POST'])
def add_urls():
    if request.method == 'POST':
        
        urls = request.json.get('urls', [])
        
    elif request.method == 'GET':
        return jsonify({"message": "This endpoint accepts POST requests."}), 200


    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    for url in urls:
        try:
            cur.execute("""
                INSERT INTO media_urls (url) VALUES (%s) ON CONFLICT (url) DO NOTHING
            """, (url,))
            conn.commit()  
        except Exception as e:
            conn.rollback()  
            return jsonify({"error": str(e)}), 500

    cur.close()
    conn.close()
    return jsonify({"message": "URLs added successfully"}), 201

if __name__ == '__main__':
    init_db()  
    app.run(host='0.0.0.0', port=8001)  



