from mongoengine import *
from flask import *
import datetime
import time

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
	date = DateTimeField(required=True, default=datetime.datetime.utcnow)   


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
				'product_description' : product.product_description
			}
			productsList.append(productDict)
		return productsList
		
		
	def get_singelProduct(self,productId):
		product = Product.objects(pk = productId )
		productDict = {}
		if product:
			product = product.get(pk = productId )   
			productDict = {
				'_id': str(product.pk),
				'product_name': product.product_name,
				'available_unit': product.available_unit,
				'per_unit_charge': product.per_unit_charge,
				'product_image': product.product_image,
				'product_description' : product.product_description
			} 

		return {
			"Success" : True,
			"product": productDict
		}   
		


	def add_user_order(self, user_email, product_Id, product_amount, total_price, date):
		# add new record to UserOrder table with these arguments
		user_order = UserOder(user_email=user_email, product_Id=product_Id, product_amount=product_amount, total_price=total_price, date=date)
		user_order.save()
		return {"Success" : True}              #successfully added the user_order


	def get_all_user_orders(self, user_email):
		#returne users all orders details  with all feild in a list of dictionary  [{}, {} ]
		orders = UserOder.objects(user_email=user_email)                     #getting all user orders
		ordersList = []                                 #list to store order details
		for order in orders:                         #looping through all orders
			orderDict = {                              #creating a dictionary for each order
				'_id': str(order.pk),
				'user_email': order.user_email,
				'product_Id': order.product_Id,
				'product_amount': order.product_amount,
				'total_price': order.total_price,
				'date' : order.date
			}
			ordersList.append(orderDict)
		return ordersList	
	

	def add_to_cart(self, user_email, product_Id, product_amount, total_price):
		product = Product.objects(pk = product_Id)                                          #searching the product with that product_Id 
		if product:
			new_available_unit = product[0].available_unit - product_amount                                                                         #if product exists with that product_id                                                 
			product.update(available_unit = new_available_unit)
			user_cart = UserCart.objects(user_email = user_email, product_Id = product_Id ) #searching if any  record is present with same user_email and product_Id  in cart table 
			if user_cart:
				new_product_amount = user_cart[0].product_amount + product_amount
				new_total_price = user_cart[0].total_price + total_price                                                                   #if this cart is already present                                                                            
				user_cart.update(product_amount = new_product_amount, total_price = new_total_price)        #adding product_amount and total price with that record
				return {"Success": True}
			else:                                                                                           #if user_cart is not present
				user_cart = UserCart(user_email=user_email, product_Id=product_Id, product_amount=product_amount, total_price=total_price)	 
				user_cart.save()
				return {"Success": True}
		else:
			return {"Success":False}

	
	def remove_from_cart(self, user_email,product_Id):
		user_cart = UserCart.objects(user_email=user_email, product_Id=product_Id)                            
		if len(user_cart) > 0:
			product_amount = user_cart[0].product_amount               #getting the product_amount from cart table
			user_cart.delete()
			reIncreasingProduct = self.increase_product(productId=product_Id, amount=product_amount)      #adding it to product by calling increase_product() method                                              #then delete the record
			return {"Success": True}
		else:
			return {"Success":False}	








  
  			




					  