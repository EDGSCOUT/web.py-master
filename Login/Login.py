#coding:utf-8
""" Basic blog using webpy 0.3 """
import web
import MySQLdb
import model
### Url mappings

urls = (
    '/', 'Index',
    '/Login','Login',
)

### Templates
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', globals=t_globals)


class Index:
    def GET(self):
        """ Show page """
        return render.Login()
class Login:
    def POST(self):
        data=web.input()
        username=data.pop('username')
        print(username)
        password=data.pop('password')
        print(password)
        print(data)
        '''conn = MySQLdb.connect(cursorclass=MySQLdb.cursors.DictCursor, db='blog', user='root', passwd='ccpl_817', host='192.168.8.3', port=3306,charset='utf8')
        cur=conn.cursor()
        cur.execute('select * from users')
        r=cur.fechall()
        print(r)
        '''
        r=model.get_user(username,password)
        wrong={"code":404}
        right={"code":200}
        if(r==None):
            #web.header('Content-Type', 'application/json')
            return json.dumps(wrong)
        else:
            #web.header('Content-Type', 'application/json')
            return json.dumps(right)


app = web.application(urls, globals())
if __name__ == '__main__':
    app.run()