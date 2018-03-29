import web, datetime

db = web.database(dbn='mysql', db='blog', user='root',pw='ccpl_817',host='192.168.8.3',port=3306,charset='utf8')

def get_posts():
    return db.select('entries', order='id DESC')

def get_user(username,password):
    try:
        return db.select('users', where='username=$username and password=$password', vars=locals())[0]
    except IndexError:
        return None

def new_hr(appuuid,apphr,apphrtime):
    try:
        return db.