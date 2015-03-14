import Settings
import tornado.web
import tornado.httpserver
import tornado.escape

import os

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/rename", RenameHandler),
            (r"/upload", UploadHandler)
        ]
        settings = {
            "template_path": Settings.TEMPLATE_PATH,
            "static_path": Settings.STATIC_PATH,
        }
        tornado.web.Application.__init__(self, handlers, **settings)

        print("Running minCloud on port %d" % Settings.PORT)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """Print dirs and files from current root."""
        listroot = os.path.join(Settings.CLOUD_PATH, self.get_argument('dir', ''))
        parentdir = os.path.split(self.get_argument('dir', ''))[0]
        dirs = []
        files = []

        for item in os.listdir(listroot):
            if os.path.isdir(os.path.join(listroot, item)) == True:
                # dirs[Directory name][Relative path to directory]
                dirs.append([item, os.path.join(self.get_argument('dir', ''), item)])
            else:
                # files[File name][Relative path to file]
                files.append([item, os.path.join(self.get_argument('dir', ''), item)])

        self.render("index.html", title="minCloud", parentdir=parentdir, currentdir=self.get_argument('dir', ''), dirs=dirs, files=files)

class RenameHandler(tornado.web.RequestHandler):
    def post(self):
        """Basic renaming for files and folders."""
        path = self.get_argument('path', '')
        target = self.get_argument('target', '')
        name = self.get_argument('name', '')
        os.rename(os.path.join(Settings.CLOUD_PATH, path, target), os.path.join(Settings.CLOUD_PATH, path, name))

        obj = { 
            'new_path': os.path.join(path, name) 
        }
        self.write(tornado.escape.json_encode(obj))

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        """Upload file(s)."""
        dirname = self.get_argument('root', '')
        for i in range(len(self.request.files['file'])):
            fileinfo = self.request.files['file'][i]
            fh = open(os.path.join(Settings.CLOUD_PATH, dirname, fileinfo['filename']), 'wb')
            fh.write(fileinfo['body'])
        
        self.redirect("/")

def main():
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(Settings.PORT)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()