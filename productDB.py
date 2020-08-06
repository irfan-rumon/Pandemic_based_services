from mongoengine import *


class ProductGeneral(Document):
    product_name = StringField(max_length=100)
    available_unit = FloatField()
    per_unit_charge = FloatField()
    product_image = StringField(max_length=1000)
    product_description = StringField(max_length=1000)

