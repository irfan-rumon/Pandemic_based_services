from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from userDB import UserGeneralDb
auth = Blueprint("auth",__name__, static_folder="static", template_folder="templates")

authDb = UserGeneralDb()

# shows  signup page
@auth.route("/getSignup", methods =["GET"])
def getSignup():
    return render_template("signup.html")


#   add a new user to database . if error  redirects to getsignup view
@auth.route("/postSignup", methods =["POST"])
def postSignup():
    
    # print(request.form.get('UserName'))

    # user Roles  Which can be accepted . 
    valid_User_Roles = set(['customer', 'doctor', 'admin'])
    # checking if UserRole is valid from form submisson 
    if request.form.get('UserRole') not in  valid_User_Roles:
        flash("This Role is not accepted ")
        return redirect(url_for('auth.getSignup'))


    try:
        
        success =  authDb.signup(user_name=request.form.get('UserName'),user_email=request.form.get('UserEmail'), user_password=request.form.get('UserPassword'), user_role=request.form.get('UserRole'))
        if success["success"]:
            flash("You have successfully signed up ")
        else:
            flash("Error during SignUp Try again  ")
    except Exception as e:
        print( "exception: " + str(e))

    
    return redirect(url_for('auth.getSignup'))

    

# shows  login page
@auth.route("/getLogin", methods =["GET"])
def getLogin():
    return render_template("login.html")


# login a new user  if error redirects to getLog in view
@auth.route("/postLogin", methods =["POST"])
def postLogin():
    print(request.form.get('UserPassword'))

    try:
        LoggedInUser = authDb.login(user_email=request.form.get('UserEmail'), user_password=request.form.get('UserPassword'))
        print(LoggedInUser['success'] )
        if LoggedInUser['success']:
            print("usermatched")
            session['UserEmail'] = LoggedInUser['userEmail']
            session['UserName'] = LoggedInUser['userName']
            session['UserRole'] = LoggedInUser['userRole']
            return redirect(url_for('index'))
        else:
            flash("Error during log in .Try again ")
    except Exception as e:
        print(str(e))
        pass


    return redirect(url_for('auth.getLogin'))



# clears all session . then  redircts to getLogin view    
@auth.route("/getLogout", methods =["GET"])
def getLogout():
    session.clear()
    
    return redirect(url_for('auth.getLogin'))