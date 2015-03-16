import configparser
import os

# Get main path from current file
dirname = os.path.dirname(__file__) 

configParser = configparser.RawConfigParser()   
configParser.read(os.path.join(dirname, 'config.ini'))

# Default port is 9999
PORT = configParser.getint('server', 'port') if configParser.get('server', 'port').isdigit() else 9999
# Default storing path is cloudstore, located in the same folder as this file
CLOUD_PATH = configParser.get('path', 'store') if configParser.get('path', 'store') else os.path.join(dirname, 'cloudstore')

STATIC_PATH = os.path.join(dirname, 'static')
TEMPLATE_PATH = os.path.join(dirname, 'templates')