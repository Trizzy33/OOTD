from flask import Blueprint, redirect, request, session, render_template, url_for, flash
from flask import jsonify
# from flask_login import  current_user, login_user, login_required, logout_user
from OOTD.views.database import *
from OOTD.templates import *
from OOTD.settings import db, gcached_table
main = Blueprint("main", __name__)


@main.route('/')
def home():
    item_data = get_rank_products(gcached_table)
    return render_template('index.html', loggedIn=False, item_data=item_data)


@main.route('/blog')
def blog():
    item_data = get_rand_blog()
    return render_template('blog.html', loggedIn=False, item_data=item_data)


@main.route("/category", methods=["POST"])
def category():
    category_form = request.form
    gender = category_form["gender"]
    master_category = category_form["master-category"]
    subcategory = category_form["sub-category"]
    article_style = category_form["article-style"]
    try:
        add_category(gender, master_category, subcategory, article_style)
    except Exception as err:
        print(err)
        return render_template("index1.html", add_category_result="failure")

    return render_template("index1.html", add_category_result="success")


@main.route('/product', methods=["POST"])
def product():
    product_form = request.form
    year = product_form["year"]
    product_name = product_form["product-name"]
    category_id = product_form["category-id"]
    product_url = product_form["product-url"]

    try:
        add_product(year, category_id, product_name, product_url)
    except Exception as err:
        print(err)
        return render_template("index1.html", add_product_result="failure")

    return render_template("index1.html", add_product_result="success")


# @main.route('/search_product', methods=["GET", "POST"])
# def search_product():
#     search_product_form = request.form
#     product_name = search_product_form["product-name"]
#     print(product_name)
#     results = find_product(product_name)
#     return render_template("index1.html", title="search_product", results=results)


@main.route("/search_username", methods=["POST"])
def search_username():
    search_username_form = request.form
    username = search_username_form["username"]
    results = find_user(username)
    return render_template("index1.html", title="search_username", results=results)


@main.route("/list_outfits", methods=["POST"])
def list_outfits():
    outfits_form = request.form
    results = get_outfits()
    return render_template("index1.html", results=results)


@main.route('/delete_outfit', methods=["POST"])
def delete_outfit():
    delete_outfit_form = request.form
    outfit_id = delete_outfit_form["outfit-id"]
    print(outfit_id)
    try:
        del_outfit(outfit_id)
    except:
        return render_template("index1.html", del_outfit_result="failure")
    return render_template("index1.html", delete_outfit_result="success")


@main.route('/list_adv1', methods=["GET", "POST"])
def list_adv1():
    results = adv1()
    return render_template("index1.html", title="adv1", results=results)


@main.route('/list_adv2', methods=["GET", "POST"])
def list_adv2():
    results = adv2()
    return render_template("index1.html", title="adv2", results=results)


# root page, route should be '/'
@main.route('/root')
def root():
    render_template('index1.html')


@main.route('/search', methods=["POST"])
def search_product():
    search_product_form = request.form
    product_name = search_product_form["product_name"]
    search_category = search_product_form["search_category"]
    print(search_category)
    item_data = search_product_name(product_name, search_category)
    # for data in item_data:
    #     print(data[1])
    return render_template('display.html',item_data=item_data, exist_item=True)
    # except:
    #     return render_template('index1.html')


@main.route('/display_category/<int:id>')
def display_category(id):
    if id == 1:
        search = "gender = 'Men'"
    elif id == 2:
        search = "gender = 'Women'"
    item_data = search_product_cate(search)
    return render_template('display.html', item_data=item_data, exist_item=True)


@main.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    results = auto_complete(search)
    results = [mv[0] for mv in results.all()]
    return jsonify(matching_results=results)


@main.route('/single/<int:product_id>')
def show_info(product_id):
    # get your list of valves from wherever it comes from
    update_rank_global(product_id)
    item_data = get_product_byID(product_id)
    exist_item = False
    if item_data is not None:
        exist_item = True
    comment_data = get_comment(product_id)
    a = comment_data.fetchone()
    
    if 'email' in session:
        update_rank_local(product_id)
        return render_template('single.html', item_data=item_data, comment_data = a, exist_item = exist_item,loggedIn=True,
                           user_name=session["user_name"])
    else:
        return render_template('single.html', item_data=item_data, comment_data = a, exist_item=exist_item, loggedIn=False)

@main.route('/rate_product', methods=['GET','POST'])
def rate_product():
    form = request.form
    rating = form["rating"]
    prev_url = request.referrer
    product_id = prev_url[prev_url.rfind('/')+1:]
  
    if 'email' not in session:
        error_msg = "Please log in first"
        return render_template('login.html', error=error_msg)
    else:
        #add rating to database
        user_email = session['email']

        user_id = find_userid(user_email).first()[0]
        style_id = find_productStyle(product_id).first()[0]

        try:
            rated_outfit(rating, product_id, user_id, style_id)
        except Exception as err:
            print(err)
            flash('You have already added this product')
            return redirect(request.referrer)

        flash('Added to your outfits successfully')
        return redirect(request.referrer)
       