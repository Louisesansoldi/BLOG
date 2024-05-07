from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt
import jwt
import os
from dotenv import load_dotenv
# from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


load_dotenv()

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
# Récupérer la clé secrète à partir des variables d'environnement
# JWT_SECRET = os.getenv('JWT_SECRET')
print(app.config['JWT_SECRET_KEY'])
# jwt = JWTManager(app)

mysql = MySQL()
mysql.init_app(app)



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

    # # Générer le token JWT
    # token = jwt.encode({'id': result[0], 'email': email}, jwt_secret, algorithm='HS256')
    # return jsonify({'token': token}), 200

    token = create_access_token(identity={'id': result[0], 'email': email})
    return jsonify({'token': token}), 200



# _________________________ UNIVERSE _________________________ 


@app.route('/api/universe', methods=['POST'])
def universe():
    data = request.get_json()
    titleUniverse = data['titleUniverse']
    backgroundUniverse = data['backgroundUniverse']
    descriptionUniverse = data['descriptionUniverse']

    print(titleUniverse)

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO universe (titleUniverse, backgroundUniverse, descriptionUniverse) VALUES (%s, %s, %s)", (titleUniverse, backgroundUniverse, descriptionUniverse))
    mysql.connection.commit()

    return jsonify({'message': 'This is your universe'}), 201



# _________________________ POSTS _________________________ 


@app.route('/api/posts', methods=['POST'])
# @jwt_required() # l'utilisateur est authentifié
def posts():
    data = request.get_json()
    user_id = get_jwt_identity() # Récupérez l'identifiant de l'utilisateur authentifié
    title = data['title']
    image = data['image']
    imageTitle = data['imageTitle']
    content = data['content']
    link= data['link']

    print(title)

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO posts (title, image, imageTitle, content, link) VALUES (%s, %s, %s, %s, %s)", (title, image, imageTitle, content, link))
    mysql.connection.commit()

    return jsonify({'message': 'Posted !'}), 201




if __name__ == '__main__':
    app.run(debug=True)


