from flask import Blueprint, redirect, request, render_template
from OOTD.settings import *

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
    print(year, product_name)
    return render_template("index.html", title="product")

