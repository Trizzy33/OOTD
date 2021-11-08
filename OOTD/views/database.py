# database manipulate
from OOTD.settings import db


# search product, return id
def product_search(product_name: str):
    conn = db.connect()
    query = "select id from product where name = '{}';".format(product_name)
    result = conn.execute(query).fetchall
    conn.close()
    id = result.first()[0]
    print(id)
    return id


# add category
def add_category(gender: str, master_cate: str, sub_cate: str, article: str):
    conn = db.connect()
    query = 'insert into category values ("{}","{}","{}","{}");'.format(
        gender, master_cate,sub_cate, article)
    conn.execute(query)
    conn.close()


# add product
def add_product(year, cate_id, product_name, product_url):
    conn = db.connect()
    query = 'insert into product(year, category_id, name, url) values("{}","{}","{}","{}");'.format(
        year, cate_id, product_name, product_url
    )
    conn.execute(query)


# update user name
def add_uname(old_name, new_name):
    conn = db.connect()
    query = 'update user set name = "{}" where name = "{}";'.format(new_name, old_name)
    conn.execute(query)
    conn.close()


# delete outfit
def del_outfit(outfit_id):
    conn = db.connect()
    query = 'delete from outfits where id = "{}";'.format(outfit_id)
    conn.execute(query)
    conn.close()
