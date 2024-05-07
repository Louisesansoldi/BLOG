from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL()
mysql.init_app(app)

# Récupérer la clé secrète à partir des variables d'environnement
JWT_SECRET = os.getenv('JWT_SECRET')

# _________________________ TEST _________________________ 
@app.route("/")
def hello_world():
    return "<p>Hello, World!!!!!!! ehehehe</p>"

# _________________________ REGISTER _________________________ 
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
    mysql.connection.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# _________________________ LOGIN _________________________ 
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result is None or not bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Charger le secret JWT à partir des variables d'environnement
    jwt_secret = os.getenv('JWT_SECRET')
    if jwt_secret is None:
        return jsonify({'message': 'JWT secret not found'}), 500

    # Générer le token JWT
    token = jwt.encode({'id': result[0], 'email': email}, jwt_secret, algorithm='HS256')
    return jsonify({'token': token.decode('utf-8')}), 200

if __name__ == '__main__':
    app.run(debug=True)
