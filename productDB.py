from mongoengine import *

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

















					  