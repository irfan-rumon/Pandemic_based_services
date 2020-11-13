from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from homeNursingDB import HomeNursingDb
from middleware import is_loggedIn, has_permission 
from datetime import datetime
from uploadUtils import photos
from nurseDB import NurseDb

homeNurse = Blueprint("homeNurse",__name__, static_folder="static", template_folder="templates")

# nurseDb = HomeNursingDb()

nurseDb = NurseDb()


@homeNurse.route("/getAddNurseinfo", methods =["GET"])
def getAddNurseinfo():
    return render_template("nurse_signup.html")


@homeNurse.route("/postAddNurseinfo", methods =["POST"])
def postAddNurseinfo():
    now = datetime.now()
    name = now.strftime("%m%d%Y%H%M%S")
    name = name+ "."

    if 'UserImage' in request.files:
        filename = photos.save(request.files['UserImage'],name=name)

    try:

        
        result = nurseDb.addnurses(image=filename,
        name =session['UserName'] , 
        phone = str(session['UserPhone']), 
        area = request.form.get('Area'), 
        certification_experience = request.form.get('Certification'),
        charge =int(request.form.get('PerUnitCharge')))

    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    
    session.clear()
    
    return redirect(url_for('auth.getLogin'))
    

@homeNurse.route("/getAllNurseinfo", methods =["GET"])
def getAllNurseinfo():

    result = None
    try:

        result = nurseDb.get_all_nurses()
    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    print(result)


    return "<h1>success</h1>"           # need to attach with frontend 




@homeNurse.route("/getSingelNurseinfo/<nurse_phone>", methods =["GET"])
def getSingelNurseinfo(nurse_phone):

    result = None
    try:

        result = nurseDb.get_single_nurse(nurse_phone)
    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    try:

        comment = nurseDb.get_all_nurse_comments(nurse_phone=nurse_phone)
    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))


    print(result)

    return "<h1>success</h1>"      # need to attach with frontend 


@homeNurse.route("/psottADDNurseComment/", methods =["GET"])
def psottADDNurseComment():


    nurse_phone = request.form.get('nurse_phone')
    comment = request.form.get('nurse_phone')

    if( str(nurse_phone) ==str(session['UserPhone'])):
        flash("You cannot  comment in your profile")
        
        # need to redirect to comment page

    result = None
    try:

        result = nurseDb.add_comment(nurse_phone=nurse_phone, user_phone= str(session['UserPhone']), user_name=session['UserName'], commnet=comment)
    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    print(result)

    return "<h1>success</h1>"      # need to redirect with frontend 





# old code starts here

@homeNurse.route("/postAddNurse", methods =["Post"])
def postAddNurse():

    city = request.form.get('city'),
    city = city[0]
    nurseNumber = request.form.get('nurseNumber')
    nurseNumber = int(nurseNumber)

    try:
        result =  nurseDb.add_nurses(city, nurseNumber)
        if result["Success"]:
            flash("Nurse added")
    except Exception as e:
        
        flash("Error try again")

    print(city )
    print(nurseNumber)


    return redirect(url_for('admin.getAdminDashBoard'))

 
@homeNurse.route("/getNurseService", methods =["GET"])
def getNurseService():

    return render_template("nurseHomePage.html")


@homeNurse.route("/postBookNurse", methods =["Post"])
@is_loggedIn 
def postBookNurs():
    city = request.form.get('city')
    date = request.form.get('date')
    address = request.form.get('address')

    cityNurseNumber = nurseDb.nursesNumberInCity(city=city)
    print(cityNurseNumber)

    alreadyBookedNurseNumber= nurseDb.get_number_bookedNurses(city=city,date=date)
    print(alreadyBookedNurseNumber)


    if alreadyBookedNurseNumber<cityNurseNumber :
        bookNurse = nurseDb.bookNurse(
        city=city,
        user_email=session['UserEmail'], 
        address=address,  
        date=date, 
        done=False
        )

        flash("Order for home Nursing is taken. Nurse will be at your place on due time.Please call 01XXXXXXXXX for details or if you face any problem")
    
    else:
        flash(" Sorry no nurse is free at your  area within the due date")

    return redirect(url_for('homeNurse.getNurseService'))


# After this need to  connect whit frontend

# Users all nurses 
@homeNurse.route("/getUsersBookedNurses", methods =["GET"])
@is_loggedIn 
def getUsersBookedNurses():

    users_all_nurses = nurseDb.get_users_booked_nurses(user_email=session['UserEmail'])
    print(users_all_nurses)

    return render_template("user_nursing_history.html", Orders = users_all_nurses)


# all booked nurses record whose done== false
@homeNurse.route("/getAllPendingNurses", methods =["GET"])
@is_loggedIn 
@has_permission('admin') 
def getAllPendingNurses():

    nurses= nurseDb.get_pending_bookedNurses()
    print(nurses)

    return render_template("admin_nursingPending.html",Orders = nurses)

# remove a booked nurse
@homeNurse.route("/getRemoveBookedNurses/<nurse_Id>", methods =["GET"])
@is_loggedIn 
def getRemoveBookedNurses(nurse_Id):

    try:
        nurse = nurseDb.remove_bookedNUrse(nurse_Id)
        flash("Your order removed successfully")
    except Exception as e:
        flash("Error try again")



    return redirect(url_for('homeNurse.getNurseService'))

# make done = True to booked Nurse entry
@homeNurse.route("/getChangeBookedNursesDone/<nurse_Id>", methods =["GET"])
@is_loggedIn 
@has_permission('admin') 
def getChangeBookedNursesDone(nurse_Id):

    try:
        nurse = nurseDb.change_pending_bookedNurses(bookedNurse_id=nurse_Id, done=True)
        flash("Completed 1 bookedNurses Service")
    except Exception as e:
        flash("Error try again")



    return redirect(url_for('homeNurse.getNurseService'))

