from mongoengine import *
from flask import *
import datetime
import time

class CitynursesNumber(Document):
	city = StringField(max_length=100)
	total_nurses = IntField()

class BookedNurses(Document):
	city = StringField(max_length=100)
	user_email = StringField(max_length=100)
	address = StringField(max_length=100)
	date = DateTimeField(required=True)
	done = BooleanField(default=False)

class HomeNursingDb():

	def __init__(self):
		pass

	def add_nurses(self, city, num):
		nurses = CitynursesNumber.objects(city=city)    #first check if there is previous nurses in that city in CitynursesNumber table
		if len(nurses) > 0:                                 #if previously nurses exists in that city
			new_total_nurses = nurses[0].total_nurses + num
			nurses[0].update(total_nurses = new_total_nurses)       #add number to  total_nurses field
		else:
			citynursesNumber = CitynursesNumber(city=city, total_nurses=num)      #create new CitynursesNumber object	 
			citynursesNumber.save()   
		return {"Success" : True}

	
	def nursesNumberInCity(self, city):
		nurses = CitynursesNumber.objects(city=city)
		return nurses[0].total_nurses          #returns number of nurses in that city


	def bookNurse(self, city, user_email, address,  date, done):
		bookedNurse = BookedNurses(city=city, user_email=user_email, address=address, date=date, done=done)   #create new entry to  bookedNurses field
		bookedNurse.save()               
		return {"Success" : True}


	def get_number_bookedNurses(self, city, date):  
		cnt_nurses = BookedNurses.objects(city=city, date= date)
		return len(cnt_nurses)                           #returns number of entries mathched with given city in bookedNurses   

	def remove_bookedNUrse(self, bookedNurse_id ):
		nurses = BookedNurses.objects()
		nurse = nurses.get( pk = bookedNurse_id )
		if len(nurse) > 0:
			nurse.delete()
			return {"Success" : True}
		else:
			 return {"Success" : False}


	def get_users_booked_nurses(self, user_email):
		nurses = BookedNurses.objects(user_email=user_email)    #contains nurses mathched with user_email from bookedNurses  
		nurseList = []                                          #list to store bookednurse details

		for nurse in nurses:
			nurseDict = {                               #creating a dictionary for each cart
				   '_id': str(nurse.pk),
				   'city': nurse.city,
				   'user_email': nurse.user_email,
				   'address': nurse.address,
				   'date': nurse.date,
				   'done': nurse.done
			}
			nurseList.append(nurseDict)
		return nurseList

	def get_pending_bookedNurses(self):
		nurses = BookedNurses.objects(done=False)                   #getting all entries from bookedNurses which  done == false       
		nurseList = []                                          #list to store bookednurse details

		for nurse in nurses:
			nurseDict = {                                    #creating a dictionary with pending nurses
				   '_id': str(nurse.pk),
				   'city': nurse.city,
				   'user_email': nurse.user_email,
				   'address': nurse.address,
				   'date': nurse.date,
				   'done': nurse.done
			}
			nurseList.append(nurseDict)
		return nurseList


	def change_pending_bookedNurses(self, bookedNurse_id, done):
		nurses = BookedNurses.objects( pk = bookedNurse_id )
		nurse = nurses.get( pk = bookedNurse_id )   

		if len(nurse) > 0:
			nurse.update(done=done)        #changing done field of the entry of bookedNurses_id table according to done
			return {"Success" : True}
		else:
			return {"Success" : False}
		
		                          

	def get_all_bookedNurses(self):   
		nurses = BookedNurses.objects()                        #getting all entries from bookedNurses      
		nurseList = []                                          #list to store bookednurse details

		for nurse in nurses:
			nurseDict = {                                    #creating a dictionary with pending nurses
				   '_id': str(nurse.pk),
				   'city': nurse.city,
				   'user_email': nurse.user_email,
				   'address': nurse.address,
				   'date': nurse.date,
				   'done': nurse.done
			}
			nurseList.append(nurseDict)
		return nurseList 
