from flask import Blueprint, redirect, request, render_template
from OOTD.settings import *
from OOTD.views.database import *
main = Blueprint("main", __name__)


@main.route('/')
def home():
    return render_template('index.html', title="template")


@main.route('/category', methods=['GET', 'POST'])
def category():
    category_form = request.form
    gender = category_form["gender"]
    master_category = category_form["master-category"]
    subcategory = category_form["sub-category"]
    article_style = category_form["article-style"]
    print(gender, master_category, subcategory, article_style)
    return render_template("index.html", title="category")


@main.route('/product', methods=["GET", "POST"])
def product():
    product_form = request.form
    year = product_form["year"]
    product_name = product_form["product-name"]
    product_url = product_form["product-url"]
    print(year, product_name, product_url)
    return render_template("index.html", title="product")


@main.route('/search_product', methods=["GET", "POST"])
def search_product():
    search_product_form = request.form
    product_name = search_product_form["product-name"]
    print(product_name)
    product_search(product_name)
    return render_template("index.html", title="search_product")


@main.route('/update_username', methods=["GET", "POST"])
def update_username():
    update_username_form = request.form
    ori_name = update_username_form["ori-name"]
    new_name = update_username_form["new-name"]
    print(ori_name, new_name)
    return render_template("index.html", title="update_username")


@main.route('/delete_outfit', methods=["GET", "POST"])
def delete_outfit():
    delete_outfit_form = request.form
    outfit_id = delete_outfit_form["outfit-id"]
    print(outfit_id)
    return render_template("index.html", title="delete_outfit")
