from flask import Flask, render_template, request, redirect
from mongoengine import connect
from mongoengine.errors import NotUniqueError
from userDB import UserGeneral

app = Flask(__name__)


connect(db='cse499', host='localhost', port=27017)


@app.route('/')
def index():
    return "This is a web baseded service platform related to pandemic"


@app.route('/signup_test')
def tester():
    user = UserGeneral(email="jko@gmail.com")
    is_valid_signUp =  user.signup( user_name = "irfan", user_email = "irgannisho8571@gmail.com", user_password = "abc", user_role = "doctor")
    return is_valid_signUp
    

if __name__ == "__main__":
    app.run(debug=True)    