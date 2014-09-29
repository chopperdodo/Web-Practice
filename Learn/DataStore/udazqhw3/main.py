#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import db

import webapp2
import jinja2
import os

# initialize jinja
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def blog_key(name = "default"):
    return db.Key.from_path('blogs', name)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    blog_title   = db.StringProperty(required = True)
    blog_content = db.TextProperty(required = True)
    blog_created = db.DateTimeProperty(auto_now_add = True)
    blog_lastModify = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        self._render_text = self.blog_content.replace('\n', '<br>')
        return render_str("post.html", blog = self)

class MainHandler(Handler):
    def render_front(self):
        blogs = db.GqlQuery("SELECT * FROM Blog "
                            "ORDER BY blog_created DESC")

        self.render("main.html", blogs=blogs)

    def get(self):
        self.render_front()

class WriteHandler(Handler):
    def render_front(self, blog_title="", blog_content="", blog_error=""):
        self.render("write.html", blog_title=blog_title,
                    blog_content=blog_content, error=blog_error)

    def get(self):
        self.render_front()
    def post(self):
        pass
        blog_title = self.request.get("subject")
        blog_content = self.request.get("content")

        if blog_title and blog_content:
            b = Blog(parent=blog_key(), blog_title=blog_title, blog_content=blog_content)
            b.put()

            self.redirect("/blog/%s" % str(b.key().id()))

        else:
            error = "we need a title for your blog!"
            self.render_front(blog_title, blog_content, error)

class Permalink(Handler):
    def get(self, blog_id):
        key = db.Key.from_path('Blog', int(blog_id), parent=blog_key())
        cur_blog = db.get(key)

        if not cur_blog:
            self.error(404)
            return

        self.render("sing_blog.html", blog=cur_blog)

app = webapp2.WSGIApplication([
                                ('/blog/?', MainHandler),
                                ('/blog/newpost', WriteHandler),
                                ('/blog/([0-9]+)', Permalink)
                              ], debug=True)
