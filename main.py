'''
Created on Mar 27, 2019

@author: liuweiyin
'''

import tornado.ioloop
import tornado.web
import os
import json


class FileUploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<html>
  <head><title>Upload File</title></head>
  <body>
    <h1>Hello Tornado Webservice!</h1>
  </body>
</html>
''')

    def post(self):
        ret = {'result': 'OK'}
        upload_path = os.path.join(os.path.dirname(__file__), 'files')  # 文件的暂存路径
        file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据

        if not file_metas:
            ret['result'] = 'Invalid Args'
            return ret

        for meta in file_metas:
            filename = meta['filename']
            file_path = os.path.join(upload_path, filename)

            with open(file_path, 'wb') as up:
                up.write(meta['body'])
                # OR do other thing

        self.write(json.dumps(ret))


class CustomDirUploadHandler(FileUploadHandler):
    def post(self):
        ret = {'result': 'OK'}
        upload_path = '/home/lwylys/workspace/wall/tf'  # 文件的暂存路径
        file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据

        if not file_metas:
            ret['result'] = 'Invalid Args'
            return ret

        for meta in file_metas:
            filename = meta['filename']
            file_path = os.path.join(upload_path, filename)

            with open(file_path, 'wb') as up:
                up.write(meta['body'])
                # OR do other thing

        self.write(json.dumps(ret))


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/file', FileUploadHandler),
        (r'/mydir', CustomDirUploadHandler)
    ])

    server = tornado.httpserver.HTTPServer(app, max_buffer_size=524288000, max_body_size=524288000)  # 10G
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
