from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from middleware import is_loggedIn, has_permission




test = Blueprint("test",__name__, static_folder="static", template_folder="templates")



@test.route("/demo", methods =["GET"])
@is_loggedIn                               # cheking if the user is logged in
@has_permission('customer','admin')        #checking if user has permisson for this route
def demo():
    # userEmail =  session['UserEmail']
    # print(userEmail)
    return 'this is a test file' 
