import Settings
import tornado.web
import tornado.httpserver

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
        root = os.path.join(Settings.CLOUD_PATH, self.get_argument('dir', ''))
        dirs = []
        files = []

        for item in os.listdir(root):
            if os.path.isdir(os.path.join(root, item)) == True:
                dirs.append(item)
            else:
                files.append(item)

        self.render("index.html", title="minCloud", root=self.get_argument('dir', ''), dirs=dirs, files=files)

class RenameHandler(tornado.web.RequestHandler):
    def post(self):
        """Basic renaming for files and folders."""
        root = self.get_argument('root', '')
        name = self.get_argument('name', '')
        new_name = self.get_argument('new_name', '')
        os.rename(os.path.join(Settings.CLOUD_PATH, root, name), os.path.join(Settings.CLOUD_PATH, root, new_name))
        
        self.redirect("/")

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