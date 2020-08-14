from mongoengine import *
from flask import Flask, render_template, request, redirect, Blueprint

class Product(Document):
	product_name = StringField(max_length=100)
	available_unit = IntField()
	per_unit_charge = FloatField()
	product_image = StringField(max_length=1000)
	product_description = StringField(max_length=1000)


class UserCart(Document): 
	user_email = EmailField(required=True)
	product_Id = StringField(max_length=1000)
	product_amount = IntField()
	total_price = FloatField()


class UserOder(Document):
	user_email = EmailField(required=True) 
	product_Id = StringField(max_length=1000)
	product_amount = IntField()
	total_price = FloatField()
	date = DateField()    


class ProductDb():

	def __init__(self):
		pass	

	def add_product(self, product_name, available_unit, per_unit_charge, product_image, product_description):
		#add produts  to product tabel
		product = Product(product_name=product_name, available_unit=available_unit, per_unit_charge=per_unit_charge, product_image=product_image, product_description=product_description)
		product.save()
		return {"Success" : True}     #successfully added the product

	def increase_product(self, productId, amount): 
		#add  amount to availabe_unit field for given productId to product table
		product = Product.objects(pk = productId )
		if product:                                     #product found with that productId 
			product = product.get(pk = productId )
			newAmount = product.available_unit + amount
			product.update(available_unit = newAmount)
			return {"Success" : True}                   #successfully incresed amount of that product
		else:                                           #No product found with that productId
			return {"Success" : False}

	def get_all_products(self):
		#return all products detail in a  list with  all Field including pk.		
		products = Product.objects()                     #getting all products
		productsList = []                                #list to store product details
		for product in products:                         #looping through all products
			productDict = {                              #creating a dictionary for each product
				'_id': str(product.pk),
				'product_name': product.product_name,
				'available_unit': product.available_unit,
				'per_unit_charge': product.per_unit_charge,
				'product_image': product.product_image,
				'product.description' : product.product_description
			}
			productsList.append(productDict)
		return render_template('show_products.html', products = productsList)	

	def add_user_order(self, user_email, product_Id, product_amount, total_price, date):
		# add new record to UserOrder table with these arguments
		user_order = UserOder(user_email=user_email, product_Id=product_Id, product_amount=product_amount, total_price=total_price, date=date)
		user_order.save()
		return {"Success" : True}              #successfully added the user_order














					  