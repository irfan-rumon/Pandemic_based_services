from mongoengine import *


class Ambulance(Document):
    image = StringField(max_length=100, required=True)
    name = StringField(max_length=100, required=True)
    phone = StringField(max_length=100, required=True)
    area = StringField(max_length=100, required=True)
    
    

class Ambulance_comment(Document):
	ambulance_phone = StringField(max_length=100)
	user_phone = StringField(max_length=100)
	user_name = StringField(max_length=100)
	comment = StringField(max_length=100)

class AmbulanceDb():
    def __init__(self):
        pass   

    def addAmbulance(self, image, name, phone, area):
        #print(phone)
        ambulance = Ambulance.objects(phone = phone )
        
        if ambulance:
            return {"success": True}
        else:
            new_ambulance = Ambulance(image=image, name=name, phone=str(phone), area=area)
            new_ambulance.save()
            recent_added_ambulance = Ambulance.objects(phone = phone )
            if recent_added_ambulance:
                return {"success": True}
            else:
                return {"success": False}



    def get_all_ambulance(self):
        ambulances = Ambulance.objects()
        ambulanceList = []
        if len(ambulances) > 0:                                 			                                            
            for ambulance in ambulances:                             
                ambulanceDict = {                              
                   '_id': str(ambulance.pk),
                   'image': ambulance.image,
                   'name': ambulance.name,
                   'phone': ambulance.phone,
                   'area': ambulance.area
                }
                ambulanceList.append(ambulanceDict)
        return ambulanceList	            
                  
    def get_single_ambulance(self, phone):
        ambulances = Ambulance.objects(phone = phone)
        ambulance_info = [] 
        if ambulances:
            ambulance = ambulances[0]
            ambulanceDict = {                              
                   '_id': str(ambulance.pk),
                   'image': ambulance.image,
                   'name': ambulance.name,
                   'phone': ambulance.phone,
                   'area': ambulance.area
            }
            ambulance_info.append(ambulanceDict)
        return ambulance_info


    def add_comment(self, ambulance_phone, user_phone, user_name, comment): 
        ambulance_comment = Ambulance_comment(ambulance_phone=ambulance_phone, user_phone=user_phone, user_name=user_name, comment=comment)
        ambulance_comment.save()
        return {"success": True}


    def get_all_ambulance_comments(self, ambulance_phone):
        comments = Ambulance_comment.objects( ambulance_phone = ambulance_phone )
        commentList = []
        if len(comments) > 0:                                 			                                            
            for ambulance_comment in comments:
                commentDict = {                              
				   '_id': str(ambulance_comment.pk),
				   'ambulance_phone': ambulance_comment.ambulance_phone,
				   'user_phone': ambulance_comment.user_phone,
				   'user_name': ambulance_comment.user_name,
				   'comment': ambulance_comment.comment
				}
                commentList.append(commentDict)
        return commentList  


