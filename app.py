from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt
import jwt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'blog_database'

mysql = MySQL(app)

# _________________________ TEST _________________________ 
@app.route("/")
def hello_world():
    return "<p>Hello, World!!!!!!! ehehehe</p>"


# _________________________ LOGIN _________________________ 

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user is None or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({'message': 'Invalid email or password'}), 401

    token = jwt.encode({'id': user['id'], 'email': user['email']}, 'your_jwt_secret', algorithm='HS256')
    return jsonify({'token': token.decode('utf-8')}), 200

if __name__ == '__main__':
    app.run(debug=True)