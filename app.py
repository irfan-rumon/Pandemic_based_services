from flask import Flask, render_template, request, redirect, Blueprint
from mongoengine import connect
from mongoengine.errors import NotUniqueError
from userDB import UserGeneral

from auth import auth
from test import test


app = Flask(__name__)
app.secret_key = "abc"  

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(test, url_prefix="/test")

connect(db='cse499', host='localhost', port=27017)


@app.route('/')
def index():
    
    return render_template("home.html")


@app.route('/signup_test')
def signup_tester():
    user = UserGeneral(email="irfannisho8571@gmail.com")
    is_valid_signUp =  user.signup( user_name = "irfan", user_email = "irfannisho8571@gmail.com", user_password = "abc", user_role = "doctor")
    return is_valid_signUp
    
@app.route('/login_test')
def login_tester():
    user = UserGeneral(email="minhaj@gmail.com")
    return user.login("minhaj@gmail.com", "abc")    

if __name__ == "__main__":
    app.run(debug=True)    