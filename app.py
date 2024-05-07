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
    name = data['name']
    email = data['email']
    password = data['password']

    # Hasher le mot de passe et le stocker en tant que chaîne de caractères
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
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

    # Vérifier si le mot de passe haché existe et correspond au mot de passe fourni
    if result is None or not bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Charger le secret JWT à partir des variables d'environnement
    jwt_secret = os.getenv('JWT_SECRET')
    if jwt_secret is None:
        return jsonify({'message': 'JWT secret not found'}), 500

    # Générer le token JWT
    token = jwt.encode({'id': result[0], 'email': email}, jwt_secret, algorithm='HS256')
    return jsonify({'token': token}), 200


# _________________________ POSTS _________________________ 


@app.route('api/posts', methods=['POST'])
def posts():
    data = request.get_json()
    title = data['title']
    image = data['image']
    imageTitle = data['imageTitle']
    content = data['content']
    link= data['link']

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO posts (title, image, imageTitle, content, link) VALUES (%s, %s, %s, %s, %s)", (title, image, imageTitle, content, link))
    mysql.connection.commit()

    return jsonify({'message': 'Posted !'}), 201
s















if __name__ == '__main__':
    app.run(debug=True)


