from mongoengine import *


class Product(Document):
    product_name = StringField(max_length=100)
    available_unit = FloatField()
    per_unit_charge = FloatField()
    product_image = StringField(max_length=1000)
    product_description = StringField(max_length=1000)

class UserCart(Documet): 
	user_email = EmailField(required=True)
	product_Id = StringField(max_length=1000)
	product_amount = FloatField()
	total_price = FloatField()

class UserOder(Document):
	user_email = EmailField(required=True) 
	product_Id = StringField(max_length=1000)
	product_amount = FloatField()
	total_price = FloatField()
	date = DateField()    

