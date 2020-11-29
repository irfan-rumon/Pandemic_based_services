from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from middleware import is_loggedIn, has_permission 
from datetime import datetime
from uploadUtils import photos
from ambulanceDB import AmbulanceDb

ambulance = Blueprint("ambulance",__name__, static_folder="static", template_folder="templates")

# nurseDb = HomeNursingDb()

ambulanceDb = AmbulanceDb()


@ambulance.route("/getAddAmbulanceinfo", methods =["GET"])
def getAddAmbulanceinfo():
    

    return render_template("ambulance_signup.html")


@ambulance.route("/postAddAmbulanceinfo", methods =["POST"])
def postAddAmbulanceinfo():
    now = datetime.now()
    name = now.strftime("%m%d%Y%H%M%S")
    name = name+ "."

    if 'UserImage' in request.files:
        filename = photos.save(request.files['UserImage'],name=name)

    try:

        
        result = ambulanceDb.addAmbulance(image=filename,
        name =session['UserName'] , 
        phone = str(session['UserPhone']), 
        area = request.form.get('Area')
        )

    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    
    session.clear()
    
    return redirect(url_for('auth.getLogin'))
    

@ambulance.route("/getAllAmbulanceinfo", methods =["GET"])
def getAllAmbulanceinfo():

    result = None
    try:

        result = ambulanceDb.get_all_ambulance()
    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    print(result)


    return render_template("ambulance_all.html", result = result)            




@ambulance.route("/getSingelAmbulanceinfo/<ambulance_phone>", methods =["GET"])
def getSingelAmbulanceinfo(ambulance_phone):

    result = None
    try:

        result = ambulanceDb.get_single_ambulance(ambulance_phone)
    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    try:

        comment = ambulanceDb.get_all_ambulance_comments(ambulance_phone)
    except Exception as e:
        flash(" Error try again")
        print( "exception: " + str(e))
        

    # print(comment)

    return render_template("ambulance_Details.html", result = result[0], comment = comment)      


@ambulance.route("/postADDAmbulanceComment/", methods =["POST"])
@is_loggedIn 
def postADDAmbulanceComment():


    ambulance_phone = request.form.get('Pphone')
    comment = request.form.get('Ucommnet')

    if( str(ambulance_phone) ==str(session['UserPhone'])):
        flash("You cannot  comment in your profile")
        
        # need to redirect to comment page

        return redirect(url_for('ambulance.getSingelAmbulanceinfo', ambulance_phone =str(ambulance_phone) ))

    result = None
    try:

        result = ambulanceDb.add_comment(ambulance_phone=ambulance_phone, user_phone= str(session['UserPhone']), user_name=session['UserName'], comment=comment)
        
    except Exception as e:
        flash( "Error try again ")
        print( " exception: " + str(e))


    return redirect(url_for('ambulance.getSingelAmbulanceinfo', ambulance_phone =str(ambulance_phone) ))      # need to redirect with frontend 


@ambulance.route("/gethospitalMap", methods =["GET"])
def gethospitalMap():
    return render_template("hospital_map.html")   


