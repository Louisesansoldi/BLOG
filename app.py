from flask import Flask, request, jsonify, abort
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
    email = get_jwt_identity() # Récupérer l'adresse e-mail de l'utilisateur authentifié
    titleUniverse = data['titleUniverse']
    backgroundUniverse = data['backgroundUniverse']
    descriptionUniverse = data['descriptionUniverse']

    cursor = mysql.connection.cursor()
    # Sélectionner l'ID de l'utilisateur à partir de son adresse e-mail
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cursor.fetchone()[0]  # Récupérer l'ID de l'utilisateur
    cursor.close()

    print("Logged in as:", email)

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO universe (titleUniverse, descriptionUniverse, backgroundUniverse, user_id) VALUES (%s, %s, %s, %s)", (titleUniverse, descriptionUniverse, backgroundUniverse, user_id))
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
@jwt_required() # l'user est authentifié
def get_universe(id):
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

# _________________________ UPDATE UNIVERSE _________________________                  PROBLEM ?

@app.route('/api/universe/<int:id>', methods=['PUT'])
@jwt_required() # l'utilisateur est authentifié
def update_universe(id):
    data = request.get_json()
    email = get_jwt_identity() # Récupérer l'adresse e-mail de l'utilisateur authentifié

    # Récupérer l'ID de l'utilisateur à partir de son adresse e-mail
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id_row = cursor.fetchone()

    # Vérifier si un ID d'utilisateur a été trouvé
    if user_id_row is None:
        abort(404, description="Utilisateur introuvable")

    user_id = user_id_row[0]  # Récupérer l'ID de l'utilisateur
    cursor.close()

    # Vérifier si l'utilisateur a le droit de mettre à jour cet univers
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT user_id FROM universe WHERE id = %s", (id,))
    result = cursor.fetchone()

    if not result or result[0] != user_id:
        abort(403, description="Vous n'êtes pas autorisé à mettre à jour cet univers")

    # Mettre à jour l'univers
    titleUniverse = data.get('titleUniverse')
    backgroundUniverse = data.get('backgroundUniverse')
    descriptionUniverse = data.get('descriptionUniverse')

    cursor.execute("UPDATE universe SET titleUniverse = %s, backgroundUniverse = %s, descriptionUniverse = %s WHERE id = %s", (titleUniverse, backgroundUniverse, descriptionUniverse, id))
    mysql.connection.commit()

    return jsonify({'message': 'Mise à jour de l\'univers réussie'}), 200


# _________________________ POSTS _________________________ 


@app.route('/api/posts', methods=['POST'])
@jwt_required() # l'utilisateur est authentifié
def posts():
    data = request.get_json()
    email = get_jwt_identity() # Récupérer l'adresse e-mail de l'utilisateur authentifié

    cursor = mysql.connection.cursor()
    # Sélectionner l'ID de l'utilisateur à partir de son adresse e-mail
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cursor.fetchone()[0]  # Récupérer l'ID de l'utilisateur
    cursor.close()

    title = data['title']
    image = data['image']
    imageTitle = data['imageTitle']
    content = data['content']
    link= data['link']
    

    print("Logged in as:", email)

    print(title)

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO posts (title, image, imageTitle, content, link, user_id, universe_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (title, image, imageTitle, content, link, user_id, universe_id))
    mysql.connection.commit()

    return jsonify({'message': 'Posted !'}), 201

# _________________________ GET POSTS _________________________ 
    
    
@app.route('/api/posts/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM posts WHERE user_id = %s", (user_id,))
    user_posts = cursor.fetchall()
    cursor.close()

    if user_posts:
        # Format the posts data into a JSON response
        posts_data = []
        for post in user_posts:
            post_data = {
                'id': post[0],
                'title': post[1],
                'image': base64.b64encode(post[2]).decode('utf-8'),
                'imageTitle': post[3],
                'content': post[4],
                'link': post[5],
                'user_id': post[6]  # Assuming user_id is the 7th column in your table
            }
            posts_data.append(post_data)

        return jsonify({'user_id': user_id, 'posts': posts_data}), 200
    else:
        return jsonify({'message': 'No posts found for user with ID {}'.format(user_id)}), 404


# _________________________ DELETE POSTS _________________________ 

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    email = get_jwt_identity()

    # Récupérer l'ID  à partir de son adresse e-mail
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id = cursor.fetchone()

    if user_id is None:
        cursor.close()
        return jsonify({'message': 'User not found'}), 404

    # Vérifier si l'utilisateur est l'auteur du post à supprimer
    cursor.execute("SELECT user_id FROM posts WHERE id = %s", (post_id,))
    post_author_id = cursor.fetchone()

    if post_author_id is None:
        cursor.close()
        return jsonify({'message': 'Post not found'}), 404

    if post_author_id[0] != user_id[0]:
        cursor.close()
        return jsonify({'message': 'you cannot delete this post'}), 403

    # Supprimer le post de la base de données
    cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Post deleted successfully'}), 200



# _________________________ ADD POSTS TO MY UNIVERSE FROM ANOTHER ONE _________________________ 

@app.route('/api/posts/<int:post_id>/copy_to_universe/<int:universe_id>', methods=['POST'])
@jwt_required() # L'utilisateur est authentifié
def add_post_from_another_one(post_id, universe_id):
    # Récupérer l'adresse e-mail de l'utilisateur authentifié
    email = get_jwt_identity()

    # Vérifier si le post existe dans l'univers source
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    source_post = cursor.fetchone()
    cursor.close()

    if not source_post:
        return jsonify({'message': 'Source post not found'}), 404

    # Vérifier si l'univers cible existe
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM universe WHERE id = %s", (universe_id,))
    target_universe = cursor.fetchone()
    cursor.close()

    if not target_universe:
        return jsonify({'message': 'Target universe not found'}), 404

    # Récupérer l'ID de l'utilisateur à partir de son adresse e-mail
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user_id_row = cursor.fetchone()

    if not user_id_row:
        return jsonify({'message': 'User not found'}), 404

    user_id = user_id_row[0]  # Récupérer l'ID de l'utilisateur
    cursor.close()

    # Copier le post de l'univers source vers l'univers cible
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO posts (title, image, imageTitle, content, link, user_id, universe_id) "
    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
     (source_post[1], source_post[2], source_post[3], source_post[4], source_post[5], user_id, universe_id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Post copied to universe successfully'}), 200




# _________________________ POST COMMENTS _________________________ 


@app.route('/api/comments/<int:posts_id>', methods=['POST'])
@jwt_required() # l'utilisateur est authentifié
def comments(posts_id):
    data = request.get_json()
    email = get_jwt_identity()  # Récupérer l'adresse e-mail de l'utilisateur authentifié

    # Récupérer le nom de l'utilisateur à partir de l'adresse e-mail
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name FROM users WHERE email = %s", (email,))
    user_name_row = cursor.fetchone()

    # Récupérer l'id de l'utilisateur à partir de l'adresse e-mail
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    users_id_row = cursor.fetchone()


    # Vérifier si un nom d'utilisateur a été trouvé
    if user_name_row is None:
        return jsonify({'message': 'Utilisateur introuvable'}), 404

    user_name = user_name_row[0]  # Récupérer le nom de l'utilisateur
    cursor.close()

    users_id = users_id_row[0]  # Récupérer l'id de l'utilisateur
    cursor.close()

    # Récupérer le contenu du commentaire
    contentComments = data.get('contentComments')

    # Insérer le commentaire dans la base de données
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO comments (user_name, contentComments, users_id, posts_id) VALUES (%s, %s, %s, %s)", (user_name, contentComments, users_id, posts_id))
    mysql.connection.commit()

    return jsonify({'message': 'Commentaire posté !'}), 201

# _________________________ GET COMMENTS _________________________ 

@app.route('/api/comments/<int:posts_id>', methods=['GET'])
@jwt_required() # l'utilisateur est authentifié
def get_comments(posts_id):
    # Récupérer les données de l'univers
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, user_name, contentComments FROM comments WHERE posts_id = %s", (posts_id,))
    comments_data = cursor.fetchall()
    cursor.close()

    comments = []
    if comments_data:
        for comment_data in comments_data:
            comment = {
                'id': comment_data[0],
                'user_name': comment_data[1],
                'contentComments': comment_data[2],
            }
            comments.append(comment)

        return jsonify(comments), 200
    else:
        return jsonify({'message': 'No comments found for post with ID {}'.format(posts_id)}), 404

# _________________________ ADD LIKES _________________________ 

@app.route('/api/posts/<int:posts_id>/likes', methods=['POST'])
@jwt_required()
def like_post(posts_id):
    # Vérifier si le post existe
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM posts WHERE id = %s", (posts_id,))
    post = cursor.fetchone()
    cursor.close()

    if not post:
        return jsonify({'message': 'Post not found'}), 404

    # Incrémenter le nombre de likes pour le post
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO likes (posts_id, likes_count) VALUES (%s, 1) ON DUPLICATE KEY UPDATE likes_count = likes_count + 1", (posts_id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'Post liked successfully'}), 200

# _________________________ GET LIKES _________________________ 

@app.route('/api/posts/<int:posts_id>/likes', methods=['GET'])
def get_likes(posts_id):
    # Exécuter une requête SQL pour compter le nombre de likes pour le post spécifié
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM likes WHERE posts_id = %s", (posts_id,))
    like_count = cursor.fetchone()[0]  # Récupérer le résultat de la requête
    cursor.close()

    # Retourner le nombre de likes sous forme de réponse JSON
    return jsonify({'post_id': posts_id, 'like_count': like_count}), 200


    

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


