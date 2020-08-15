from flask import Flask, render_template, request, redirect, Blueprint
from mongoengine import connect
from mongoengine.errors import NotUniqueError
from uploadUtils import photos
from flask_uploads import  configure_uploads

from productDB import Product, ProductDb
import datetime
import time
from auth import auth
from test import test
from admin import admin
from shop import shop

app = Flask(__name__)
app.secret_key = "abc"  

   # import this  before uploading files from any other py files 

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app,photos)


app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(test, url_prefix="/test")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(test, url_prefix="/shop")

connect(db='cse499', host='localhost', port=27017)

productDb = ProductDb()


@app.route('/')
def index():
	
	return render_template("home.html")

@app.route('/addProduct_test')
def addProduct():
	return productDb.add_product(product_name="hand gloves", available_unit = 25, per_unit_charge = 15.00, product_image = "jkjjdf.jpeg", product_description = "This is hand gloves")

 
@app.route('/increaseProduct_test')
def increaseProduct():
	return productDb.increase_product("5f2e893cb21bfbc8153df3c8", 2009)   


@app.route('/getAllProducts_test')
def getAllProducts():
	return productDb.get_all_products()


@app.route('/addUserOrder_test')
def addUserOrder():
	return productDb.add_user_order(user_email="irfannisho8571@gmail.com", product_Id="5f2e893cb21bfbc8153df3c8", product_amount = 2, total_price=50, date=datetime.datetime.utcnow)


if __name__ == "__main__":
	app.run(debug=True)    