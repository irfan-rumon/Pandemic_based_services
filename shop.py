from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from productDB import ProductDb
shop = Blueprint("shop",__name__, static_folder="static", template_folder="templates")

productDb = ProductDb()

@shop.route("/getAllProducts", methods =["GET"])
def getAllProducts():

    productList = productDb.get_all_products()

    return render_template('allProducts.html',products = productList['products'])


@shop.route("/getProductDetails/<product_Id>", methods =["GET"] )
def getProductDetails(product_Id):

    productDetails = productDb.get_singelProduct(product_Id)
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