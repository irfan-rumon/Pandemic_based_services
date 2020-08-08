from flask import Flask, render_template, request, redirect, Blueprint
from mongoengine import connect
from mongoengine.errors import NotUniqueError
from productDB import ProductDb

from auth import auth
from test import test


app = Flask(__name__)
app.secret_key = "abc"  

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(test, url_prefix="/test")

connect(db='cse499', host='localhost', port=27017)

productDb = ProductDb()


@app.route('/')
def index():
    return "This is a web baseded service platform related to pandemic"

@app.route('/addProduct_test')
def addProduct():
    return productDb.add_product(product_name="hand gloves", available_unit = 25, per_unit_charge = 15.00, product_image = "jkjjdf.jpeg", product_description = "This is hand gloves")
       

if __name__ == "__main__":
    app.run(debug=True)    