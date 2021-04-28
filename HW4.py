from flask import Flask, request, send_from_directory, render_template,session, request, flash, redirect,url_for
from flask_login import login_required, login_user, LoginManager, UserMixin,logout_user
from flask_pymongo import PyMongo
app = Flask(__name__)
app.secret_key = b'mongo'
login_manager = LoginManager()
login_manager.init_app(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/users"
mongo = PyMongo(app)

class User(UserMixin):
    def __init__(my, username, password):
        my.password = password
        my.username = username

    def is_active(my):
        return True
    
    def get(my,username):
        if my.username == username:
            return my
        else:
            return None

    def get_id(my):
        return my.username
        
def check(username,password,saved_password):
    if password == saved_password:
        return User(username,password)
    else:
        return None
        
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = mongo.db.user.find_one({"username": username})
        if user is not None:
            user = check(username,password,user['password'])
        if user is not None:
            user = login_user(user)
            return redirect(url_for('cabinet'))
    return render_template('auth.html')

@app.route('/cabinet')
@login_required
def cabinet():
    return render_template("HW3.html")
    #"Hello, %s!" % auth.username()
    
@app.route('/static/<path:path>')
def index13(path):
    return send_from_directory('static', path)

    
@login_manager.user_loader
def index2(username):
    user = mongo.db.user.find_one({"username": username})
    if user is not None:
        return User(username,user['password'])
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)    