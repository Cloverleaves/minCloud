import Settings
import tornado.web
import tornado.httpserver
import tornado.escape

import os
import time
import mimetypes

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/mkdir", MkdirHandler),
            (r"/rename", RenameHandler),
            (r"/download", DownloadHandler),
            (r"/delete", DeleteHandler),
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
                # files[File name][Relative path to file][Modified on]
                item_rel_path = os.path.join(self.get_argument('dir', ''), item)
                item_abs_path = os.path.join(Settings.CLOUD_PATH, self.get_argument('dir', ''), item)
                (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(item_abs_path)
                files.append([item, item_rel_path, str(Helper.sizeof_fmt(size)), str(mtime)])

        self.render("index.html", title="minCloud", parentdir=parentdir, currentdir=self.get_argument('dir', ''), dirs=dirs, files=files)

class MkdirHandler(tornado.web.RequestHandler):
    def post(self):
        path = self.get_argument('path', '')
        directory = self.get_argument('directory', '') # New directory name
        if not os.path.exists(os.path.join(Settings.CLOUD_PATH, path, directory)):
            os.mkdir(os.path.join(Settings.CLOUD_PATH, path, directory))

        self.redirect("/?dir=" + path)

class RenameHandler(tornado.web.RequestHandler):
    def post(self):
        """Basic renaming for files and folders."""
        path = self.get_argument('path', '')
        target = self.get_argument('target', '')
        name = self.get_argument('name', '')
        os.rename(os.path.join(Settings.CLOUD_PATH, path, target), os.path.join(Settings.CLOUD_PATH, path, name))

class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        """Upload file(s)."""
        path = self.get_argument('path', '')
        for i in range(len(self.request.files['file'])):
            fileinfo = self.request.files['file'][i]
            fh = open(os.path.join(Settings.CLOUD_PATH, path, fileinfo['filename']), 'wb')
            fh.write(fileinfo['body'])
        
        self.redirect("/?dir=" + path)

class DownloadHandler(tornado.web.RequestHandler):
    def get(self):
        """Download file by get method."""
        path = self.get_argument('path', '')
        target = self.get_argument('target', '')

        content_type = mimetypes.guess_type(target)
        file = open(os.path.join(Settings.CLOUD_PATH, path, target) , 'r')
        self.set_header('Content-Type', content_type[0] if content_type[0] is not None else 'text/plain') # Fix for invalid mime-types
        self.set_header('Content-Disposition', 'attachment; filename=' + target + '')
        self.write(file.read())
        

class DeleteHandler(tornado.web.RequestHandler):
    def post(self):
        path = self.get_argument('path', '')
        target = self.get_argument('target', '')
        os.remove(os.path.join(Settings.CLOUD_PATH, path, target))

class Helper(object):
    def sizeof_fmt(num, suffix='B'):
        """Return human readable size."""
        for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

def main():
    applicaton = Application()
    http_server = tornado.httpserver.HTTPServer(applicaton)
    http_server.listen(Settings.PORT)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()