from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from testDB import TestDB
from middleware import is_loggedIn, has_permission 
from datetime import datetime

testSample = Blueprint("testSample",__name__, static_folder="static", template_folder="templates")

sampleTestDb = TestDB()


@testSample.route("/postAddCollector", methods =["Post"])
@is_loggedIn    
@has_permission('admin') 

def postAddCollector():

    city = request.form.get('city'),
    city = city[0]
    collectorNumber = request.form.get('collectorNumber')
    collectorNumber = int(collectorNumber)

    try:
        result =  sampleTestDb.add_test(city, collectorNumber)
        if result["Success"]:
            flash("sampel collectors  added")
    except Exception as e:
        
        flash("Error try again")

    print(city )
    print(collectorNumber)


    return redirect(url_for('admin.getAdminDashBoard'))

 
@testSample.route("/getTestService", methods =["GET"])
def getTestService():

    return render_template("TestHomePage.html")


@testSample.route("/postBookSample", methods =["Post"])
@is_loggedIn 
def postBookSample():
    city = request.form.get('city')
    date = request.form.get('date')
    address = request.form.get('address')

    citySampleNumber = sampleTestDb.testNumberInCity(city=city)
    print(citySampleNumber)

    alreadyBookedSampleNumber= sampleTestDb.get_number_bookedTest(city=city,date=date)
    print(alreadyBookedSampleNumber)


    if alreadyBookedSampleNumber<citySampleNumber :
        bookTest = sampleTestDb.bookTest(
        city=city,
        user_email=session['UserEmail'], 
        address=address,  
        date=date, 
        done=False
        )

        flash("Order for sample collection service is taken. Volunteers will be at your place on due time.Please call 01XXXXXXXXX for details or if you face any problem")
    
    else:
        flash(" Sorry no Volunteer is free at your  area within the due date")

    return redirect(url_for('testSample.getTestService'))




 
@testSample.route("/getUsersBookedTests", methods =["GET"])
@is_loggedIn 
def getUsersBookedTests():

    users_all_tests = sampleTestDb.get_users_booked_test(user_email=session['UserEmail'])
    print(users_all_tests)

    return render_template("user_test_history.html", Orders = users_all_tests)



@testSample.route("/getAllPendingTest", methods =["GET"])
@is_loggedIn 
@has_permission('admin') 
def getAllPendingTest():

    test= sampleTestDb.get_pending_bookedTest()
    print(test)

    return render_template("admin_testPending.html",Orders = test)


@testSample.route("/getRemoveBookedTest/<test_Id>", methods =["GET"])
@is_loggedIn 
def getRemoveBookedTest(test_Id):

    try:
        test = sampleTestDb.remove_bookedTest(test_Id)  
        flash("Your order removed successfully")
    except Exception as e:
        flash("Error try again")



    return redirect(url_for('testSample.getTestService'))


@testSample.route("/getChangeBookedTestDone/<test_Id>", methods =["GET"])
@is_loggedIn 
@has_permission('admin') 
def getChangeBookedTestDone(test_Id):

    try:
        test = sampleTestDb.change_pending_bookedTest(bookedTest_id=test_Id, done=True)
        flash("Completed 1 test sample collection Service")
    except Exception as e:
        flash("Error try again")



    return redirect(url_for('testSample.getTestService'))