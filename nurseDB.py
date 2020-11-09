from mongoengine import *


class Nurse(Document):
    image = StringField(max_length=100, required=True)
    name = StringField(max_length=100, required=True)
    phone = StringField(max_length=100, required=True)
    area = StringField(max_length=100, required=True)
    certification_experience = StringField(max_length=400)
    charge = IntField()

class Nurse_comment(Document):
	nurse_phone = StringField(max_length=100)
	user_phone = StringField(max_length=100)
	user_name = StringField(max_length=100)
	comment = StringField(max_length=100)

class NurseDb():
    def __init__(self):
        pass   

    def addnurses(self, image, name, phone, area, certification_experience, charge):
        print(phone)
        nurse = Nurse.objects(phone = phone )
        
        if nurse:
            return {success: True}
        else:
            new_nurse = Nurse(image=image, name=name, phone=str(phone), area=area, certification_experience=certification_experience,charge=charge)
            new_nurse.save()
            recent_added_nurse = Nurse.objects(phone = phone )
            if recent_added_nurse:
                return {success: True}
            else:
                return {success: False}



    def get_all_nurses(self):
        nurses = Nurses.objects()
        nurseList = []
        if len(nurses) > 0:                                 			                                            
            for nurse in nurses:                             
                nurseDict = {                              
                   '_id': str(nurse.pk),
                   'image': nurse.image,
                   'name': nurse.name,
                   'phone': nurse.phone,
                   'area': nurse.area,
                   'certification_experience': nurse.certification_experience,
                   'charge': nurse.charge
                }
                nurseList.append(nurseDict)
        return nurseList	            
                  
    def get_single_nurse(self, phone):
        nurses = Nurses.objects(phone = phone)
        nurse_info = [] 
        if nurses:
            nurse = nurses[0]
            nurseDict = {                              
                   '_id': str(nurse.pk),
                   'image': nurse.image,
                   'name': nurse.name,
                   'phone': nurse.phone,
                   'area': nurse.area,
                   'certification_experience': nurse.certification_experience,
                   'charge': nurse.charge
            }
            nurse_info.append(nurseDict)
        return nurse_info


    def add_comment(self, nurse_phone, user_phone, user_name, commnet): 
        nurse_comment = Nurse_comment(nurse_phone=nurse_phone, user_phone=user_phone, user_name=user_name, comment=comment)
        nurse_comment.save()
        return {success: True}


    def get_all_nurse_comments(self, nurse_phone):
        comments = Nurse_comment.objects( nurse_phone = nurse_phone )
        commentList = []
        if len(comments) > 0:                                 			                                            
            for nurse_comment in comments:
                commentDict = {                              
				   '_id': str(nurse_comment.pk),
				   'nurse_phone': nurse_comment.nurse_phone,
				   'user_phone': nurse_comment.user_phone,
				   'user_name': nurse_comment.user_name,
				   'comment': nurse_comment.comment
				}
                commentList.append(commentDict)
        return commentList  


    def delete_commnet(self, comment_pk):    
        comments = Nurse_comment.objects( pk = comment_pk ) 
        comment = comments.get( pk = comment_pk )    

		if len(comment) > 0:
			comment.delete()
			return {"success": True}
		else:
			return {"success": False}

    
   
