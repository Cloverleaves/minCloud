import os
dirname = os.path.dirname(__file__)

PORT = 9999

BASE_PATH = os.getcwd()
STATIC_PATH = os.path.join(dirname, 'static')
TEMPLATE_PATH = os.path.join(dirname, 'templates')
CLOUD_PATH = os.path.join(dirname, 'cloudstore')