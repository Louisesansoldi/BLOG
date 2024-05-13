from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

load_dotenv()

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_IDENTITY_CLAIM'] = 'sub'
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Récupérer la clé secrète à partir des variables d'environnement
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')



jwt = JWTManager(app)

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

    token = create_access_token(identity=email)
    return jsonify({'token': token}), 200



# _________________________ CREATE UNIVERSE _________________________ 


@app.route('/api/universe', methods=['POST'])
@jwt_required() # l'utilisateur est authentifié
def universe():
    data = request.get_json()
    user_id = get_jwt_identity() # Récupérez l'identifiant de l'utilisateur authentifié
    titleUniverse = data['titleUniverse']
    backgroundUniverse = data['backgroundUniverse']
    descriptionUniverse = data['descriptionUniverse']

    print("Logged in as:", user_id)

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO universe (titleUniverse, backgroundUniverse, descriptionUniverse) VALUES (%s, %s, %s)", (titleUniverse, backgroundUniverse, descriptionUniverse))
    mysql.connection.commit()

    return jsonify({'message': 'This is your universe' }), 201


# _________________________ GET ALL UNIVERSES _________________________ 

import base64

@app.route('/api/universe', methods=['GET'])
@jwt_required() # l'utilisateur est authentifié
def get_universes():
    # Récupérer les données de l'univers
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, titleUniverse, descriptionUniverse, backgroundUniverse FROM universe")
    universes_data = cursor.fetchall()
    cursor.close()

    universes = []
    if universes_data:
        for universe_data in universes_data:
            universe = {
                'id': universe_data[0],
                'titleUniverse': universe_data[1],
                'descriptionUniverse': universe_data[2],
                # Convertir backgroundUniverse de BLOB en Base64
                'backgroundUniverse': base64.b64encode(universe_data[3]).decode('utf-8')
            }
            universes.append(universe)

        return jsonify(universes), 200
    else:
        return jsonify({'message': 'No universes found'}), 404


# _________________________ GET 1 UNIVERSE _________________________ 

@app.route('/api/universe/<int:id>', methods=['GET'])
@jwt_required() # l'utilisateur est authentifié
def get_universe(id):
    # Récupérer les données de l'univers
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, titleUniverse, descriptionUniverse, backgroundUniverse FROM universe WHERE id = %s", (id,))
    universes_data = cursor.fetchall()
    cursor.close()

    universes = []
    if universes_data:
        for universe_data in universes_data:
            universe = {
                'id': universe_data[0],
                'titleUniverse': universe_data[1],
                'descriptionUniverse': universe_data[2],
                # Convertir backgroundUniverse de BLOB en Base64
                'backgroundUniverse': base64.b64encode(universe_data[3]).decode('utf-8')
            }
            universes.append(universe)

        return jsonify(universes), 200
    else:
        return jsonify({'message': 'No universes found'}), 404

# _________________________ UPDATE UNIVERSE _________________________ 

# @app.route('/api/universe/<int:id>', methods=['PUT'])
# @jwt_required() # l'utilisateur est authentifié
# def update_universe(id):
#     data = request.get_json()
#     user_id = get_jwt_identity() # Récupérer l'identifiant de l'utilisateur authentifié

#     # Vérifier si l'utilisateur a le droit de mettre à jour cet univers
#     cursor = mysql.connection.cursor()
#     cursor.execute("SELECT user_id FROM universe WHERE id = %s", (id,))
#     result = cursor.fetchone()

#     if not result or result['user_id'] != user_id:
#         abort(403, description="Unauthorized to update this universe")

#     # Mettre à jour l'univers
#     titleUniverse = data.get('titleUniverse')
#     backgroundUniverse = data.get('backgroundUniverse')
#     descriptionUniverse = data.get('descriptionUniverse')

#     cursor.execute("UPDATE universe SET titleUniverse = %s, backgroundUniverse = %s, descriptionUniverse = %s WHERE id = %s", (titleUniverse, backgroundUniverse, descriptionUniverse, id))
#     mysql.connection.commit()

#     return jsonify({'message': 'Universe updated successfully'}), 200


# _________________________ POSTS _________________________ 


@app.route('/api/posts', methods=['POST'])
@jwt_required() # l'utilisateur est authentifié
def posts():
    data = request.get_json()
    user_id = get_jwt_identity() # Récupérez l'identifiant de l'utilisateur authentifié
    title = data['title']
    image = data['image']
    imageTitle = data['imageTitle']
    content = data['content']
    link= data['link']
    
    print("Logged in as:", user_id)
    

    print(title)

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO posts (title, image, imageTitle, content, link) VALUES (%s, %s, %s, %s, %s)", (title, image, imageTitle, content, link))
    mysql.connection.commit()

    
    return jsonify({'message': 'Posted !'}), 201
    
# _________________________ COMMENTS _________________________ 



if __name__ == '__main__':
    app.run(debug=True)


