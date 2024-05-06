# from flask import Flask
# from markupsafe import escape
# from flask import request
# from flask import render_template

# app = Flask(__name__)





# # _________________________ URL PAGE _________________________ 
# @app.route('/about')
# def about():
#     return 'The about page'

# # _________________________ HTTP METHODS _________________________ 


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()
    
#     #OR

# @app.get('/login')
# def login_get():
#     return show_the_login_form()

# @app.post('/login')
# def login_post():
#     return do_the_login()

# # _________________________ TEMPLATES _________________________

# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)