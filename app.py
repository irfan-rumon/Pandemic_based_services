from flask import Flask, render_template, request, redirect
from mongoengine import connect
from mongoengine.errors import NotUniqueError



app = Flask(__name__)

connect(db='cse499', host='localhost', port=27017)




@app.route('/')
def index():
    return "This is a web baseded service platform related to pandemic"



if __name__ == "__main__":
    app.run(debug=True)    