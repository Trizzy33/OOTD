# database manipulate
from OOTD.settings import db


# search product, return id
def product_search(product_name: str):
    conn = db.connect()
    query = "select * from product where name like '%%{}%%';".format(product_name)
    result = conn.execute(query)
    conn.close()
    # result is a cursor result object
    return result


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
    for row in result:
        print(row)
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
    for row in result:
        print(row)
