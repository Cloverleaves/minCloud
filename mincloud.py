#!/usr/bin/python3
import os
import re
import time
import shutil
import mimetypes

import tornado.web
import tornado.httpserver
import tornado.escape

from Settings import Settings
from Helper import Helper

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/mkdir", MkdirHandler),
            (r"/rename", RenameHandler),
            (r"/download", DownloadHandler),
            (r"/delete", DeleteHandler),
            (r"/upload", UploadHandler),
            (r"/view", ViewHandler)
        ]
        settings = {
            "template_path": Settings.TEMPLATE_PATH,
            "static_path": Settings.STATIC_PATH,
            "cookie_secret": Settings.COOKIE_SECRET,
            "login_url": "/login"
        }
        tornado.web.Application.__init__(self, handlers, **settings)

        print("Running minCloud on port %d" % Settings.PORT)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(BaseHandler):
    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("login.html", title="minCloud Login", errormessage=errormessage)

    def check_permission(self, password, username):
        return True if username == Settings.USERNAME and password == Settings.PASSWORD else False

    def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        auth = self.check_permission(password, username)
        if auth:
            self.set_current_user(username)
            self.redirect("/")
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Incorrect login!")
            self.redirect(u"/login" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        """Print dirs and files from current root."""
        listroot = os.path.join(Settings.CLOUD_PATH, self.get_argument('dir', ''))
        parentdir = os.path.split(self.get_argument('dir', ''))[0]
        
        dirs = []
        files = []

        for item in os.listdir(listroot):
            if os.path.isdir(os.path.join(listroot, item)):
                # dirs[Directory name][Relative path to directory]
                dirs.append([item, os.path.join(self.get_argument('dir', ''), item)])
            else:
                # files[File name][Relative path to file][Size][Modified on][Extension]
                item_rel_path = os.path.join(self.get_argument('dir', ''), item)
                item_abs_path = os.path.join(Settings.CLOUD_PATH, self.get_argument('dir', ''), item)
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(item_abs_path) # todo: deeper usage

                files.append([item, item_rel_path, str(Helper.sizeof_fmt(size)), Helper.def_date(mtime), Helper.def_extension(os.path.splitext(item_rel_path))])

        self.render("index.html", title="minCloud", parentdir=parentdir, currentdir=self.get_argument('dir', ''), dirs=dirs, files=files)

class ViewHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        """Print out the given item."""
        target = self.get_argument('target', '')
        
        content_type = mimetypes.guess_type(target)
        file = os.path.join(Settings.CLOUD_PATH, target)
        self.set_header('Content-Type', content_type[0] if content_type[0] is not None else 'text/plain') # Fix for invalid mime-types
        self.write(open(file, 'rb').read())

class MkdirHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        path = self.get_argument('path', '')
        directory = self.get_argument('directory', '') # New directory name
        
        # invalid characters: '\', '/', '"', '<', '>'
        if re.search('(\\\\|/|"|%22|<|>)', directory):
            print("Invalid dirname") # todo: notification
        else:
            if not os.path.exists(os.path.join(Settings.CLOUD_PATH, path, directory)):
                os.mkdir(os.path.join(Settings.CLOUD_PATH, path, directory))

        self.redirect("/?dir=" + tornado.escape.url_escape(path))

class RenameHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        """Basic renaming for files and folders."""
        path = self.get_argument('path', '')
        target = self.get_argument('target', '')
        name = self.get_argument('name', '')
        
        # invalid characters: '\', '/', '"', '<', '>'
        if re.search('(\\\\|/|"|%22|<|>)', name):
            print("Invalid filename") # todo: notification
        else:
            os.rename(os.path.join(Settings.CLOUD_PATH, path, target), os.path.join(Settings.CLOUD_PATH, path, name))

class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        """Upload file(s)."""
        path = self.get_argument('path', '')

        for i in range(len(self.request.files['file'])):
            fileinfo = self.request.files['file'][i]

            # invalid characters: '\', '/', '"', '<', '>'
            if re.search('(\\\\|/|"|%22|<|>)', fileinfo['filename']):
                print("Invalid filename") # todo: notification
            else:
                fh = open(os.path.join(Settings.CLOUD_PATH, path, fileinfo['filename']), 'wb')
                fh.write(fileinfo['body'])
        
        self.redirect("/?dir=" + tornado.escape.url_escape(path))

class DownloadHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        """Download file by get method."""
        path = self.get_argument('path', '')
        target = self.get_argument('target', '')

        content_type = mimetypes.guess_type(target)
        file = os.path.join(Settings.CLOUD_PATH, path, target)
        self.set_header('Content-Type', content_type[0] if content_type[0] is not None else 'text/plain') # Fix for invalid mime-types
        self.set_header('Content-Disposition', 'attachment; filename=' + target + '')
        self.write(open(file, 'rb').read())
        

class DeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        path = self.get_argument('path', '')
        target = self.get_argument('target', '')
        item = os.path.join(Settings.CLOUD_PATH, path, target)
        if os.path.isdir(item):
            shutil.rmtree(item)
        else:
            os.remove(item)

def main():
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(Settings.PORT)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
    