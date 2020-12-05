from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from burialDB import BurialDb
from middleware import is_loggedIn, has_permission 
from datetime import datetime
from uploadUtils import photos
fuService = Blueprint("fuService",__name__, static_folder="static", template_folder="templates")

fuDB = BurialDb()





@fuService.route("/getAddFUinfo", methods =["GET"])
def getAddFUinfo():
    

    return render_template("fu_signup.html")


@fuService.route("/postAddFUinfo", methods =["POST"])
def postAddFUinfo():
    now = datetime.now()
    name = now.strftime("%m%d%Y%H%M%S")
    name = name+ "."

    if 'UserImage' in request.files:
        filename = photos.save(request.files['UserImage'],name=name)

    try:

        
        result = fuDB.addBurial(image=filename,
        name =session['UserName'] , 
        phone = str(session['UserPhone']), 
        area = request.form.get('Area')
        )

    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    
    session.clear()
    
    return redirect(url_for('auth.getLogin'))
    

@fuService.route("/getAllFUinfo", methods =["GET"])
def getAllFUinfo():

    result = None
    try:

        result = fuDB.get_all_burial()
    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    # print(result)


    return render_template("fu_all.html", result = result)            




@fuService.route("/getSingelFUinfo/<FU_phone>", methods =["GET"])
def getSingelFUinfo(FU_phone):

    result = None
    try:

        result = fuDB.get_single_burial(FU_phone)
    except Exception as e:
        flash("Error try again")
        print( "exception: " + str(e))

    try:

        comment = fuDB.get_all_burial_comments(FU_phone)
    except Exception as e:
        flash(" Error try again")
        print( "exception: " + str(e))
        

    

    return render_template("fu_Details.html", result = result[0], comment = comment)      


@fuService.route("/postADDFUComment/", methods =["POST"])
@is_loggedIn 
def postADDFUComment():


    FU_phone = request.form.get('Pphone')
    comment = request.form.get('Ucommnet')

    if( str(FU_phone) ==str(session['UserPhone'])):
        flash("You cannot  comment in your profile")
        
        # need to redirect to comment page

        return redirect(url_for('fuService.getSingelFUinfo', FU_phone =str(FU_phone) ))

    result = None
    try:

        result = fuDB.add_comment(burial_phone=FU_phone, user_phone= str(session['UserPhone']), user_name=session['UserName'], comment=comment)
        
    except Exception as e:
        flash( "Error try again ")
        print( " exception: " + str(e))


    return redirect(url_for('fuService.getSingelFUinfo', FU_phone =str(FU_phone) ))      # need to redirect with frontend 




# old code starts here

@fuService.route("/postAddVolunteer", methods =["Post"])
@is_loggedIn    
@has_permission('admin') 

def postAddVolunteer():

    city = request.form.get('city'),
    city = city[0]
    collectorNumber = request.form.get('collectorNumber')
    collectorNumber = int(collectorNumber)

    try:
        result =  fuDB.add_funerals(city, collectorNumber)
        if result["Success"]:
            flash("Volunteers  added")
    except Exception as e:
        
        flash("Error try again")

    print(city )
    print(collectorNumber)


    return redirect(url_for('admin.getAdminDashBoard'))

 
@fuService.route("/getfuneralService", methods =["GET"])
def getfuneralService():

    return render_template("funeralHomePage.html")


@fuService.route("/postBookFuService", methods =["Post"])
@is_loggedIn 
def postBookFuService():
    city = request.form.get('city')
    date = request.form.get('date')
    address = request.form.get('address')

    cityFuNumber = fuDB.funeralNumberInCity(city=city)
    print(cityFuNumber)

    alreadyBookedFuNumber= fuDB.get_number_bookedFunerals(city=city,date=date)
    print(alreadyBookedFuNumber)


    if alreadyBookedFuNumber<cityFuNumber :
        fuObj = fuDB.bookFuneral(
        city=city,
        user_email=session['UserEmail'], 
        address=address,  
        date=date, 
        done=False
        )

        flash("Order for Burial and Funeral service is taken. Volunteers will be at your place on due time.Please call 01XXXXXXXXX for details or if you face any problem")
    
    else:
        flash(" Sorry no Volunteer is free at your  area within the due date")

    return redirect(url_for('fuService.getfuneralService'))




 
@fuService.route("/getUsersBookedFuService", methods =["GET"])
@is_loggedIn 
def getUsersBookedFuService():

    users_all_services = fuDB.get_users_booked_funerals(user_email=session['UserEmail'])
    print(users_all_services)

    return render_template("user_fu_service_history.html", Orders = users_all_services)



@fuService.route("/getAllPendingFuService", methods =["GET"])
@is_loggedIn 
@has_permission('admin') 
def getAllPendingFuService():

    services= fuDB.get_pending_bookedFunerals()
    print(services)

    return render_template("admin_fuService_Pending.html",Orders = services)


@fuService.route("/getRemoveFuSevice/<Order_Id>", methods =["GET"])
@is_loggedIn 
def getRemoveFuSevice(Order_Id):

    try:
        fu = fuDB.remove_bookedFuneral(Order_Id)  
        flash("Your order removed successfully")
    except Exception as e:
        flash("Error try again")



    return redirect(url_for('fuService.getfuneralService'))


@fuService.route("/getChangeBookedFuDone/<Order_Id>", methods =["GET"])
@is_loggedIn 
@has_permission('admin') 
def getChangeBookedFuDone(Order_Id):

    try:
        fu = fuDB.change_pending_bookedFunerals(bookedFuneral_id=Order_Id, done=True)
        flash("Completed 1 Burial and Funeral Service")
    except Exception as e:
        flash("Error try again")



    return redirect(url_for('fuService.getfuneralService'))