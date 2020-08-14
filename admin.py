from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from productDB import ProductDb
from uploadUtils import photos
from datetime import datetime

productDb = ProductDb()

admin = Blueprint("admin",__name__, static_folder="static", template_folder="templates")




@admin.route("/getAdminDashBoard", methods =["GET"])
def getAdminDashBoard():


    
    
    return render_template("admin.html")





@admin.route("/postAddProduct", methods =["POST"])
def postAddProduct():
    
    now = datetime.now()
    name = now.strftime("%m%d%Y%H%M%S")
    name = name+ "."

    if 'ProductImage' in request.files:
        filename = photos.save(request.files['ProductImage'],name=name)
        
        try:
            result =  productDb.add_product(product_name=request.form.get('ProductName'),
            available_unit=request.form.get('AvailableUnit'),
            per_unit_charge=request.form.get('PerUnitCharge'),
            product_description=request.form.get('ProductDescription'),
            product_image=filename)
            if result:
                flash("New Product Added ")
        except Exception as e:
                flash("Error Try again")
        
    return redirect(url_for('admin.getAdminDashBoard'))