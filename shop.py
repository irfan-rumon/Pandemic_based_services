from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from productDB import ProductDb
from middleware import is_loggedIn, has_permission 
shop = Blueprint("shop",__name__, static_folder="static", template_folder="templates")


productDb = ProductDb()

@shop.route("/getAllProducts", methods =["GET"])
def getAllProducts():

    productList = productDb.get_all_products()
    
    return render_template('allProducts.html',products = productList)


@shop.route("/getProductDetails/<product_Id>", methods =["GET"] )
def getProductDetails(product_Id):

    productDetails = productDb.get_singleProduct(product_Id)
    print(productDetails)

    return render_template('productDetail.html',product = productDetails['product'])





@shop.route("/postIncreaseProduct", methods =["POST"] )
@is_loggedIn    
@has_permission('admin') 
def postIncreaseProduct():

    product_Id  = request.form.get('id')
    amount = request.form.get('amount')
    amount = int(amount)

    productDb.increase_product(productId=product_Id, amount=amount)
    

    return redirect(url_for('shop.getProductDetails', product_Id=product_Id ))


@shop.route("/getAddToCart/<product_Id>/<product_amount>", methods =["GET"])
@is_loggedIn    
def getAddToCart(product_Id,product_amount):

    productDetails = productDb.get_singleProduct(product_Id)

    product_name = productDetails['product_name']
    total_price = productDetails['per_unit_charge'] * product_amount

    try:

        result = productDb.add_to_cart(
            user_email= session['UserEmail'],
            product_Id= product_Id,
            product_name=product_name,
            product_amount=product_amount,
            total_price=total_price)
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
                flash("Added to Cart") 
    except Exception as e:
        flash("Error Try again") 

    return redirect(url_for('shop.getAllProducts'))

