#coding:utf-8
import web
import json
urls = (
     '/', 'index'
)

app = web.application(urls, globals())

class hello:
    def GET(self, name):
        if not name:
            name = 'World'
        return 'Hello, ' + name + '!'

class index:
    def GET(self):
        pyDict = {'one':1,'two':2}
        ##web.header('Content-Type', 'application/json')
        return json.dumps(pyDict)

if __name__ == "__main__":
    app.run()

