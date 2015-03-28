#!/usr/bin/python3
import os
import configparser

class Settings(object):
    # Get main path from current file
    dirname = os.path.dirname(__file__) 

    configParser = configparser.RawConfigParser()   
    configParser.read(os.path.join(dirname, 'config.ini'))

    # Default port is 9999
    PORT = configParser.getint('server', 'port') if configParser.get('server', 'port').isdigit() else 9999

    # Paths
    # Default storing path is cloudstore, located in the same folder as this file
    CLOUD_PATH = configParser.get('path', 'store') if configParser.get('path', 'store') else os.path.join(dirname, 'cloudstore')
    STATIC_PATH = os.path.join(dirname, 'static')
    TEMPLATE_PATH = os.path.join(dirname, 'templates')

    # You should generate your own key in config.ini
    COOKIE_SECRET = configParser.get('auth', 'key') if configParser.get('auth', 'key') else "_GENERATE_YOUR_OWN_RANDOM_VALUE_"

    # Authentication
    # Default username and password: "admin"
    USERNAME = configParser.get('auth', 'username') if configParser.get('auth', 'username') else "admin"
    PASSWORD = configParser.get('auth', 'password') if configParser.get('auth', 'password') else "admin"
