from mongoengine import *


class Burial(Document):
    image = StringField(max_length=100, required=True)
    name = StringField(max_length=100, required=True)
    phone = StringField(max_length=100, required=True)
    area = StringField(max_length=100, required=True)
    
    

class Burial_comment(Document):
	burial_phone = StringField(max_length=100)
	user_phone = StringField(max_length=100)
	user_name = StringField(max_length=100)
	comment = StringField(max_length=100)

class BurialDb():
    def __init__(self):
        pass   

    def addBurial(self, image, name, phone, area):
        #print(phone)
        burial = Burial.objects(phone = phone )
        
        if burial:
            return {"success": True}
        else:
            new_burial = Burial(image=image, name=name, phone=str(phone), area=area)
            new_burial.save()
            recent_added_burial = Burial.objects(phone = phone )
            if recent_added_burial:
                return {"success": True}
            else:
                return {"success": False}



    def get_all_burial(self):
        burials = Burial.objects()
        burialList = []
        if len(burials) > 0:                                 			                                            
            for burial in burials:                             
                burialDict = {                              
                   '_id': str(burial.pk),
                   'image': burial.image,
                   'name': burial.name,
                   'phone': burial.phone,
                   'area': burial.area
                }
                burialList.append(burialDict)
        return burialList	            
                  
    def get_single_burial(self, phone):
        burials = Burial.objects(phone = phone)
        burial_info = [] 
        if burials:
            burial = burials[0]
            burialDict = {                              
                   '_id': str(burial.pk),
                   'image': burial.image,
                   'name': burial.name,
                   'phone': burial.phone,
                   'area': burial.area
            }
            burial_info.append(burialDict)
        return burial_info


    def add_comment(self, burial_phone, user_phone, user_name, comment): 
        burial_comment = Burial_comment(burial_phone=burial_phone, user_phone=user_phone, user_name=user_name, comment=comment)
        burial_comment.save()
        return {"success": True}


    def get_all_burial_comments(self, burial_phone):
        comments = Burial_comment.objects( burial_phone = burial_phone )
        commentList = []
        if len(comments) > 0:                                 			                                            
            for burial_comment in comments:
                commentDict = {                              
				   '_id': str(burial_comment.pk),
				   'burial_phone': burial_comment.burial_phone,
				   'user_phone': burial_comment.user_phone,
				   'user_name': burial_comment.user_name,
				   'comment': burial_comment.comment
				}
                commentList.append(commentDict)
        return commentList  

