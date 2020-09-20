from mongoengine import *
from flask import *
import datetime
import time

class CityTestNumber(Document):
	city = StringField(max_length=100)
	total_test = IntField()

class BookedTest(Document):
	city = StringField(max_length=100)
	user_email = StringField(max_length=100)
	address = StringField(max_length=100)
	date = DateTimeField(required=True)
	done = BooleanField(default=False)

class TestDB():

	def __init__(self):
		pass

	def add_test(self, city, num):
		test = CityTestNumber.objects(city=city)    #first check if there is previous    test in that city in CityTestNumber table
		if len(test) > 0:                                 #if previously    test exists in that city
			new_total_test =  test[0].total_test + num
			test[0].update(total_test = new_total_test)       #add number to  total_test field
		else:
			cityTestNumber = CityTestNumber(city=city, total_test=num)      #create new CityTestNumber object	 
			cityTestNumber.save()   
		return {"Success" : True}

	
	def testNumberInCity(self, city):
		test = CityTestNumber.objects(city=city)
		return    test[0].total_test          #returns number of    test in that city


	def bookTest(self, city, user_email, address,  date, done):
		bookedTest = BookedTest(city=city, user_email=user_email, address=address, date=date, done=done)   #create new entry to  bookedNurses field
		bookedTest.save()               
		return {"Success" : True}


	def get_number_bookedTest(self, city, date):  
		cnt_test = BookedTest.objects(city=city, date= date)
		return len(cnt_test)                           #returns number of entries mathched with given city in bookedNurses   

	def remove_bookedTest(self, bookedTest_id ):
		test = BookedTest.objects()
		test =   test.get( pk = bookedTest_id )
		if len(test) > 0:
			test.delete()
			return {"Success" : True}
		else:
			 return {"Success" : False}


	def get_users_booked_test(self, user_email):
		tests = BookedTest.objects(user_email=user_email)    #contains    test mathched with user_email from bookedNurses  
		testList = []                                          #list to store bookednurse details

		for test in    tests:
			testDict = {                               #creating a dictionary for each cart
				   '_id': str(test.pk),
				   'city': test.city,
				   'user_email': test.user_email,
				   'address': test.address,
				   'date': test.date,
				   'done': test.done
			}
			testList.append(testDict)
		return testList

	def get_pending_bookedTest(self):
		tests = BookedTest.objects(done=False)                   #getting all entries from bookedNurses which  done == false       
		testList = []                                          #list to store bookednurse details

		for test in  tests:
			testDict = {                                    #creating a dictionary with pending    test
				   '_id': str(test.pk),
				   'city': test.city,
				   'user_email': test.user_email,
				   'address': test.address,
				   'date': test.date,
				   'done': test.done
			}
			testList.append(testDict)
		return testList


	def change_pending_bookedTest(self, bookedTest_id, done):
		test = BookedTest.objects( pk = bookedTest_id )
		test =    test.get( pk = bookedTest_id )   

		if len(test) > 0:
			test.update(done=done)        #changing done field of the entry of bookedNurses_id table according to done
			return {"Success" : True}
		else:
			return {"Success" : False}
		
								  

	def get_all_bookedTest(self):   
		tests = BookedTest.objects()                        #getting all entries from bookedNurses      
		testList = []                                          #list to store bookednurse details

		for test in    tests:
			testDict = {                                    #creating a dictionary with pending    test
				   '_id': str(test.pk),
				   'city': test.city,
				   'user_email': test.user_email,
				   'address': test.address,
				   'date': test.date,
				   'done': test.done
			}
			testList.append(testDict)
		return testList 
