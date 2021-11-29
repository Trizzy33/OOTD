# database manipulate
from time import time
from flask import session
from OOTD.settings import db, gcached_table, app
import random

# search product, return id
def find_product(product_name: str):
    conn = db.connect()
    query = "select * from product where name like '%%{}%%';".format(product_name)
    result = conn.execute(query)
    conn.close()
    # result is a cursor result object
    return result

def get_product_byID(product_id):
    conn = db.connect()
    query = "select year, name, gender, base_color, url from product natural join style where id = {} limit 1;".format(product_id)
    result = conn.execute(query)
    conn.close()
    # result is a cursor result object
    return result


# search username
def find_user(user_email: str):
    conn = db.connect()
    query = 'select name from user where email = "{}";'.format(user_email)
    result = conn.execute(query)
    user_name = result.first()[0]
    conn.close()
    print(user_name)
    return user_name


# add category
def add_category(gender: str, master_cate: str, sub_cate: str, article: str):
    conn = db.connect()
    query = 'insert into category values ("{}","{}","{}","{}");'.format(
        gender, master_cate, sub_cate, article)
    conn.execute(query)
    conn.close()


# add product
def add_product(year, cate_id, product_name, product_url):
    conn = db.connect()
    query = 'insert into product(id, year, category_id, name, url) values("{}", "{}","{}","{}","{}");'.format(
        60001, year, cate_id, product_name, product_url
    )
    conn.execute(query)


# update user name
def update_uname(old_name, new_name):
    conn = db.connect()
    query = 'update user set name = "{}" where name = "{}";'.format(new_name, old_name)
    conn.execute(query)
    conn.close()


# get all outfits
def get_outfits():
    conn = db.connect()
    query = "select * from outfits"
    result = conn.execute(query)
    conn.close()
    return result


# delete outfit
def del_outfit(outfit_id):
    conn = db.connect()
    query = 'delete from outfits where id = "{}";'.format(outfit_id)
    conn.execute(query)
    conn.close()


# count user name
def cnt_uname():
    conn = db.connect()
    query = 'select count(*) from user'
    result = conn.execute(query)
    conn.close()
    cnt = result.first()[0]
    print(cnt)
    return cnt


# count product
def cnt_product():
    conn = db.connect()
    query = 'select count(*) from product'
    result = conn.execute(query)
    conn.close()
    cnt = result.first()[0]
    print(cnt)
    return cnt


# count user name
def cnt_category():
    conn = db.connect()
    query = 'select count(*) from category'
    result = conn.execute(query)
    conn.close()
    cnt = result.first()[0]
    print(cnt)
    return cnt


# count user name
def cnt_outfits():
    conn = db.connect()
    query = 'select count(*) from outfits'
    result = conn.execute(query)
    conn.close()
    cnt = result.first()[0]
    print(cnt)
    return cnt


# advanced query
def adv1():
    conn = db.connect()
    query = 'SELECT u.user_id, u.name, b.cnt ' \
            'FROM user u JOIN (SELECT author_id, COUNT(id) AS cnt FROM blog GROUP BY author_id) AS b ' \
            'ON user_id = author_id ' \
            'ORDER BY b.cnt DESC LIMIT 15;'
    result = conn.execute(query)
    conn.close()
    return result


def adv2():
    conn = db.connect()
    query = "(SELECT u.name, u.email, b.blog_text " \
            "FROM user u JOIN (SELECT author_id, blog_text FROM blog WHERE blog_text LIKE '%%{}%%' ) AS b " \
            "ON author_id = user_id WHERE u.gender = 'MALE' ORDER BY u.user_id) " \
            "UNION " \
            "(SELECT u.name, u.email, b.blog_text " \
            "FROM user u JOIN (SELECT author_id, blog_text FROM blog WHERE blog_text LIKE '%%{}%%' ) AS b " \
            "ON author_id = user_id WHERE u.gender = 'MALE' ORDER BY u.user_id)".format('tutu', 'disney')
    result = conn.execute(query)
    conn.close()
    return result


# return true if email and password are correct
def is_valid(email, password):
    conn = db.connect()
    query = 'SELECT COUNT(*) FROM user WHERE email = "{}" AND password = "{}";'.format(email, password)
    result = conn.execute(query)
    conn.close()
    if result.first()[0]:
        return True
    else:
        return False


# add user to database
def add_user(email, gender, password, name, dob):
    conn = db.connect()
    query = 'INSERT INTO user(name, gender, dob, email, password) VALUES ("{}","{}","{}","{}","{}") ;'.format(
        name, gender, dob, email, password
    )
    conn.execute(query)
    conn.close()


# update user info
def update_user(email, name, gender, dob):
    conn = db.connect()
    query = 'UPDATE user SET name = "{}", gender = "{}", dob = "{}" WHERE email = "{}";'.format(name,
                                                                                                gender, dob, email)
    conn.execute(query)
    conn.close()


# find user id
def find_userid(email):
    conn = db.connect()
    query = 'SELECT user_id FROM user WHERE email = "{}";'.format(email)
    result = conn.execute(query)
    conn.close()
    print(result)
    return result


# update password
def update_password(old_password, new_password, email):
    conn = db.connect()
    query = 'SELECT password FROM user WHERE email = "{}";'.format(email)
    result = conn.execute(query)
    user_password = result.first()[0]
    if old_password == user_password:
        act = 'UPDATE user SET password = "{}" WHERE email = "{}";'.format(new_password, email)
        conn.execute(act)
        conn.close()
        return True
    else:
        return False


# get user info
def get_user_info(email):
    conn = db.connect()
    query = 'SELECT name, gender, dob FROM user WHERE email = "{}";'.format(email)
    result = conn.execute(query)
    user_info = result.first()
    conn.close()
    return user_info

def get_userOufit_info(email):
    conn = db.connect()
    query = 'SELECT name, gender, dob FROM user WHERE email = "{}";'.format(email)
    result = conn.execute(query)
    user_info = result.first()
    conn.close()
    return user_info

def search_product_name(product_name, search_category):
    conn = db.connect()
    if search_category == "Women" or search_category == "Men":
        query = 'SELECT distinct name, url, id FROM product NATURAL JOIN style WHERE gender' \
                ' LIKE "%%{}%%" AND name like "%%{}%%" LIMIT 100;'.format(search_category, product_name)
    else:
        query = 'SELECT distinct name, url, id FROM product WHERE name like "%%{}%%" LIMIT 100;'.format(product_name)
    item_data = conn.execute(query)
    conn.close()
    return item_data


def get_rand_product():
    random.seed(time())
    start_id = random.randrange(0, 4000)
    conn = db.connect()
    query = 'SELECT name, url, id FROM product WHERE id > "{}" AND id < "{}";'.format(start_id, start_id+50)
    result = conn.execute(query)
    conn.close()
    return result

def search_product_cate(search):
    conn = db.connect()
    random.seed(time())
    offset = random.randrange(0, 3600)
    query = 'SELECT product.name, product.url, product.id FROM product JOIN (SELECT id FROM category WHERE {} )' \
            'AS cate ON product.category_id = cate.id LIMIT 100 OFFSET {};'.format(search, offset)
    result = conn.execute(query)
    conn.close()
    return result


def auto_complete(search):
    conn = db.connect()
    query = 'SELECT product.name FROM product WHERE name like "%%{}%%" LIMIT 10;'.format(search)
    results = conn.execute(query)
    conn.close()
    return results


def get_rand_blog():
    random.seed(time())
    start_id = random.randrange(0, 1000)
    conn = db.connect()
    query = ' SELECT user.name, blog.blog_text, product.name' \
            ' FROM project.user join project.blog on user_id = author_id join project.blog_product on id = blog_id ' \
            'join project.product on product_id = project.product.id' \
            ' WHERE blog.id > "{}" AND blog.id < "{}";'.format(start_id, start_id+20)
    result = conn.execute(query)
    conn.close()
    return result



#search product comment using product id 
def get_comment(product_id):
    conn = db.connect()
    query = "select distinct blog_text from blog natural join blog_product natural join product where id = {} limit 1;".format(product_id)
    result = conn.execute(query)
    conn.close()
    return result


def get_product_categories(product_id):
    # get product's cate_master and cate_sub
    conn = db.connect()
    query = f"""
        SELECT category.cate_master, category.cate_sub 
        FROM product JOIN category ON product.category_id = category.id 
        WHERE product.id = "{product_id}";
    """
    result = conn.execute(query)
    conn.close()
    return result

###### Recommendation Algorithm

# global ranking
def get_rank_products(table):
    categories = sorted(table.items(), key=lambda x: -x[1])
    categories = [itr[0] for itr in categories]

    products = []
    chosen = set()

    if len(categories) != 0:
        for category in categories:
            res = search_product_cate(f'cate_master = "{category}" OR cate_sub = "{category}"')
            for i, itr in enumerate(res):
                if i >= app.config["MAX_PER_CATEGORY"]:
                    break
                if itr[2] not in chosen:
                    products.append(itr)
                    chosen.add(itr[2])

    # if not enough
    if len(products) < app.config["MAX_PRODUCTS"]:
        res = get_rand_product()
        for itr in res:
            if itr[2] in chosen:
                continue
            if len(products) > app.config["MAX_PRODUCTS"]:
                break
            products.append(itr)
            chosen.add(itr[2])
    return products

def update_rank(table, category):
    if category in table:
        table[category] += 1
    elif len(table) < app.config["TOP_CATEGORIES"]:
        table[category] = 1
    else:
        for itr in table.keys():
            table[itr] -= 1
            if table[itr] == 0:
                del table[itr]

def update_rank_local(product_id):
    categories = get_product_categories(product_id)
    table = session["ucached_table"]
    for category in categories:
        update_rank(table, category[0])
        update_rank(table, category[1])
    session["ucached_table"] = table

def update_rank_global(product_id):
    categories = get_product_categories(product_id)
    for category in categories:
        update_rank(gcached_table, category[0])
        update_rank(gcached_table, category[1])

############################################
# User rating for outfits
############################################
def find_productStyle(product_id):
    conn = db.connect()
    query = 'SELECT style_id FROM product_style WHERE product_id = "{}";'.format(product_id)
    result = conn.execute(query)
    conn.close()
    print(result)
    return result

def rated_outfit(rating, product_id, user_id, style_id):
    conn = db.connect()
    rating = rating or 0.0
    query = 'insert into outfits values ("{}","{}","{}","{}");'.format(
        product_id, style_id, rating, user_id)
    conn.execute(query)
    conn.close()
    
def get_user_outfits(user_id):
    conn = db.connect()
    query = 'SELECT distinct product.name, url, product.id, user_rating FROM product JOIN outfits JOIN user JOIN style WHERE product.id = outfits.id and user.user_id = outfits.user_id and user.user_id = "{}";'.format(user_id)
    result = conn.execute(query)
    conn.close()
    return result

def get_user_rating(product_id, user_id):
    conn = db.connect()
    query = 'SELECT style_id FROM product_style WHERE product_id = "{}" AND user_id = "{};'.format(product_id, user_id)
    result = conn.execute(query)
    rating = result.first()[0]
    conn.close()
    return rating
    
def delete_outfit(user_id, outfit_id):
    conn = db.connect()
    print("outfit", outfit_id, "user",user_id)
    query = 'DELETE FROM outfits WHERE id = "{}" AND user_id = "{}";'.format(outfit_id, user_id)
    conn.execute(query)
    query = 'SELECT * FROM outfits WHERE id = "{}" AND user_id = "{}";'.format(outfit_id, user_id)
    resutls = conn.execute(query)
    print(resutls.first())
    conn.close()
