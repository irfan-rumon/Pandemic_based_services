from mongoengine import *


class UserGeneral(Document):
    name = StringField(max_length=100)
    phone = StringField(required=True)
    password = StringField(max_length=100)
    role = StringField(max_length=100)



class UserGeneralDb():

    def __init__(self):
        pass

    def signup(self, user_name, user_phone, user_password, user_role):
        """
            it firtst checks whether phone already exist in User table: 
	        if email already exist in this table  then it returns  dictionary {success: False}
	        if email doesn't exist  add new user to the data base
	        check if user is added  successfully to the database
	        if user successfully added to the database return dictionary {success: True}
        """
        currentEmail = UserGeneral.objects( phone = user_phone )
        if len(currentEmail) > 0 : #email already exists
             return {"success":False}
        else:
             user = UserGeneral()
             user.name = user_name
             user.phone = user_phone
             user.password = user_password
             user.role = user_role
             user.save()  #save the new user to database
             currentUser = UserGeneral.objects( phone = user_phone ) #recently added user's reference
             if len(currentUser) == 1 : #successfully added to the database
                 return {"success":True}
             else:
                 return {"success":False}   

    def login(self, user_phone, user_password):
        """
           check If  phone and password matches the data base
	       if doesn't match  return dictionary {success: False}
	       if match return dictionary {success: True		   
                                       userName: matched users Name
                                       userEmail: matched users email
                                       userRole: matched users Role
        """                             
        currentUser = UserGeneral.objects(phone = user_phone, password = user_password)
        if len(currentUser) == 0 :        #Email and paddwords not match
            return {"success":False}
        else:
            return {"success" : True,
                     "userName" : currentUser[0].name,
                     "userPhone" : currentUser[0].phone,
                     "userRole" : currentUser[0].role
                   }  
       