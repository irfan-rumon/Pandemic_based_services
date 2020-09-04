from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from productDB import ProductDb
from middleware import is_loggedIn, has_permission 
from datetime import datetime

shop = Blueprint("shop",__name__, static_folder="static", template_folder="templates")


productDb = ProductDb()

@shop.route("/getAllProducts", methods =["GET"])
def getAllProducts():

	productList = productDb.get_all_products()

	return render_template('allProducts.html',products = productList)


@shop.route("/getProductDetails/<product_Id>", methods =["GET"] )
def getProductDetails(product_Id):
    
	productDetails = productDb.get_singleProduct(product_Id)
	

	return render_template('productDetail.html',product = productDetails['product'])





@shop.route("/postIncreaseProduct", methods =["POST"] )
#@is_loggedIn  
#@has_permission('admin') 
def postIncreaseProduct():

	product_Id  = request.form.get('id')
	amount = request.form.get('amount')
	amount = int(amount)

	productDb.increase_product(productId=product_Id, amount=amount)
	

	return redirect(url_for('shop.getProductDetails', product_Id=product_Id ))




@shop.route("/postAddToCart", methods =["POST"])  
@is_loggedIn 
def postAddToCart():
    product_Id = request.form.get('id')
    product_amount = request.form.get('amount')


    productDetails = productDb.get_singleProduct(product_Id)
    productDetails = productDetails["product"]
    product_name = productDetails['product_name']
    total_price = productDetails['per_unit_charge'] * int(product_amount)
    
    try:

        result = productDb.add_to_cart(
            user_email= session['UserEmail'],
            product_Id= product_Id,
            product_name=product_name,
            product_amount=int(product_amount),
            total_price=total_price
            )
        if result["Success"]:
            flash("Added to Cart") 
    except Exception as e:
        flash("Error Try again") 

    return redirect(url_for('shop.getAllProducts'))



@shop.route("/getRemoveFromCart/<product_Id>", methods =["GET"])
@is_loggedIn    
def getRemoveFromCart(product_Id):
    

    try:

        result = productDb.remove_from_cart(user_email= session['UserEmail'], product_Id=product_Id)

        if result["Success"] :
            flash("Removed from cart") 
    except Exception as e:
        flash("Error Try again") 
    

    return redirect(url_for('shop.getUserCart'))




@shop.route("/getUserCart", methods =["GET"])
@is_loggedIn  
def getUserCart():

    total_amount = 0

    result = productDb.get_user_cart(user_email=session['UserEmail'] )
    for item in  result:
        total_amount  = total_amount + item["total_price"]

    return render_template("cart.html", cartItems = result, total_amount = total_amount)   # template is not added




@shop.route("/getAddOrder", methods =["GET"])
@is_loggedIn   
def getAddOrder():
    
    result = productDb.get_user_cart(user_email=session['UserEmail'] )
    now = datetime.now()
    name = now.strftime("%m%d%Y%H%M%S") 


    for item in result:

        temp = productDb.add_user_order(
            user_email = session['UserEmail'],
            product_Id =item['product_Id'] ,
            product_name = item["product_name"], 
            product_amount = item["product_amount"], 
            total_price = item["total_price"], 
            date = str(now)
            )

    flash("Your order is received. your products  will be delivered within 3 days")  
    return  redirect(url_for('shop.getAllProducts'))



@shop.route("/getUsersAllOrder", methods =["GET"])
 
def getUsersAllOrder():

    print("In all order method")

    UserOrders =  productDb.get_all_user_orders(user_email  = session['UserEmail'])

    return render_template("orderList.html", userOrders = UserOrders)   # template is not added
