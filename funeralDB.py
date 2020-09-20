from mongoengine import *
from flask import *
import datetime
import time

class CityFuneralNumber(Document):
	city = StringField(max_length=100)
	total_funerals = IntField()

class BookedFunerals(Document):
	city = StringField(max_length=100)
	user_email = StringField(max_length=100)
	address = StringField(max_length=100)
	date = DateTimeField(required=True)
	done = BooleanField(default=False)

class FuneralDb():

	def __init__(self):
		pass

	def add_funerals(self, city, num):
		funerals = CityFuneralNumber.objects(city=city)    #first check if there is previous funerals in that city in CityFuneralNumber table
		if len(funerals) > 0:                                 #if previously funerals exists in that city
			new_total_funerals = funerals[0].total_funerals + num
			funerals[0].update(total_funerals = new_total_funerals)       #add number to  total_funerals field
		else:
			cityFuneralNumber = CityFuneralNumber(city=city, total_funerals=num)      #create new CityFuneralNumber object	 
			cityFuneralNumber.save()   
		return {"Success" : True}

	
	def funeralNumberInCity(self, city):
		funerals = CityFuneralNumber.objects(city=city)
		return funerals[0].total_funerals          #returns number of funerals in that city


	def bookFuneral(self, city, user_email, address,  date, done):
		bookedFuneral = BookedFunerals(city=city, user_email=user_email, address=address, date=date, done=done)   #create new entry to  bookedNurses field
		bookedFuneral.save()               
		return {"Success" : True}


	def get_number_bookedFunerals(self, city, date):  
		cnt_funerals = BookedFunerals.objects(city=city, date= date)
		return len(cnt_funerals)                           #returns number of entries mathched with given city in bookedNurses   

	def remove_bookedFuneral(self, bookedFuneral_id ):
		funerals = BookedFunerals.objects()
		funeral = funerals.get( pk = bookedFuneral_id )
		if len(funeral) > 0:
			funeral.delete()
			return {"Success" : True}
		else:
			 return {"Success" : False}


	def get_users_booked_funerals(self, user_email):
		funerals = BookedFunerals.objects(user_email=user_email)    #contains funerals mathched with user_email from bookedNurses  
		funeralList = []                                          #list to store bookednurse details

		for funeral in funerals:
			funeralDict = {                               #creating a dictionary for each cart
				   '_id': str(funeral.pk),
				   'city': funeral.city,
				   'user_email': funeral.user_email,
				   'address': funeral.address,
				   'date': funeral.date,
				   'done': funeral.done
			}
			funeralList.append(funeralDict)
		return funeralList

	def get_pending_bookedFunerals(self):
		funerals = BookedFunerals.objects(done=False)                   #getting all entries from bookedNurses which  done == false       
		funeralList = []                                          #list to store bookednurse details

		for funeral in funerals:
			funeralDict = {                                    #creating a dictionary with pending funerals
				   '_id': str(funeral.pk),
				   'city': funeral.city,
				   'user_email': funeral.user_email,
				   'address': funeral.address,
				   'date': funeral.date,
				   'done': funeral.done
			}
			funeralList.append(funeralDict)
		return funeralList


	def change_pending_bookedFunerals(self, bookedFuneral_id, done):
		funerals = BookedFunerals.objects( pk = bookedFuneral_id )
		funeral = funerals.get( pk = bookedFuneral_id )   

		if len(funeral) > 0:
			funeral.update(done=done)        #changing done field of the entry of bookedNurses_id table according to done
			return {"Success" : True}
		else:
			return {"Success" : False}
		
								  

	def get_all_bookedFunerals(self):   
		funerals = BookedFunerals.objects()                        #getting all entries from bookedNurses      
		funeralList = []                                          #list to store bookednurse details

		for funeral in funerals:
			funeralDict = {                                    #creating a dictionary with pending funerals
				   '_id': str(funeral.pk),
				   'city': funeral.city,
				   'user_email': funeral.user_email,
				   'address': funeral.address,
				   'date': funeral.date,
				   'done': funeral.done
			}
			funeralList.append(funeralDict)
		return funeralList 
