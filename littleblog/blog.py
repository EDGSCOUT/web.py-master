#coding:utf-8
""" Basic blog using webpy 0.3 """
import web
import model

### Url mappings

urls = (
    '/', 'Index',
    '/view/(\d+)', 'View',
    '/new', 'New',
    '/login', 'Login',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
)

### Templates
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)


class Index:

    def GET(self):
        """ Show page """
        posts = model.get_posts()
        return render.index(posts)


class View:

    def GET(self, id):
        """ View single post """
        post = model.get_post(int(id))
        return render.view(post)


class Login:
    form1 = web.form.Form(
        web.form.Textbox('user', web.form.notnull,
                         size=30,
                         description="user"),
        web.form.Textarea('password', web.form.notnull,
                          size=30,
                          description="password"),
        web.form.Button('sure'),
    )
    def GET(self):
        form1 = self.form1()
        return render.new(form1)

    def POST(self):
        form1 = self.form1()
        if not form1.validates():
            return render.new(form1)
        model.new_post1(form1.d.user, form1.d.password)
        raise web.seeother('/')

class New:
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
                            size=30,
                            description="Post title:"),
        web.form.Textarea('content', web.form.notnull,
                            rows=30, cols=80,
                            description="Post content:"),
        web.form.Button('Post entry'),
    )


    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_post(form.d.title, form.d.content)
        raise web.seeother('/')


class Delete:

    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother('/')


class Edit:

    def GET(self, id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)

    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/')


app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()