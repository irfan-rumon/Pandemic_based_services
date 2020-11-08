from flask import session, redirect, url_for, flash
from functools import wraps



# decorator to check if the user is logged in 
def is_loggedIn(f):

    @wraps(f)
    def wrapper(*args, **kwds):
        if 'UserPhone' not  in session:
            flash('Please Login First')
            return redirect(url_for('auth.getLogin'))
           
        
        return f(*args, **kwds)
    return wrapper


# decorator to check if the user has permission for  a route
# arguments: roles          ( Array of user roles whaic has the permission to the  route)
def has_permission(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            if 'UserRole' not  in session:
                flash(' User don\'t have permission for this operation ')
                return redirect(url_for('auth.getLogin'))

            if  session['UserRole'] not in roles :
                flash(' User don\'t have permission for this operation ')
                return redirect(url_for('auth.getLogin'))
            
            
            return f(*args, **kwds)
        return wrapper
    return decorator