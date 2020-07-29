from mongoengine import *


class UserGeneral(Document):
    name = StringField(max_length=100)
    email = EmailField(required=True)
    password = StringField(max_length=100)
    role = StringField(max_length=100)

    def signup(self, user_name, user_email, user_password, user_role):
        """
            it firtst checks whether email already exist in User table: 
	        if email already exist in this table  then it returns  dictionary {success: False}
	        if email doesn't exist  add new user to the data base
	        check if user is added  successfully to the database
	        if user successfully added to the database return dictionary {success: True}
        """
        currentEmail = UserGeneral.objects( email = user_email )
        if len(currentEmail) > 0 : #email already exists
             return {"success":"False"}
        else:
             user = UserGeneral()
             user.name = user_name
             user.email = user_email
             user.password = user_password
             user.role = user_role
             user.save()  #save the new user to database
             currentUser = UserGeneral.objects( email = user_email ) #recently added user's reference
             if len(currentUser) == 1 : #successfully added to the database
                 return {"success":"True"}
             else:
                 return {"success":"False"}   

    def login(self, user_email, user_password):
        """
           check If  email and password matches the data base
	       if doesn't match  return dictionary {success: False}
	       if match return dictionary {success: True		   
                                       user:  matched users name	
				                     }
        """                             
        currentUser = UserGeneral.objects(email = user_email, password = user_password)
        if len(currentUser) == 0 :        #Email and paddwords not match
            return {"success":"False"}
        else:
            return {"success" : "True",
                     "user" : currentUser[0].name
                   }  
       


