import os

# for all of our configurations

# all configurations that were previously in __init__.py will go here
# e.g. previously in core __init__.py - app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# now here: SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
class Config:
    # secret key - protect from crossites requests, modifying cookies etc.
    # good way to generate - in terminal write python, then import secrets -> secrets.token_hex(16) -> gives random code 16 bytes
    # in real app - database like postgre sql - there it should be hidden in environment variable
    SECRET_KEY = '0faded5e76c8ff95553a1e5a2829d81c'
    # creating DB
    # for development its enough to use SQL LITE - simple db files in the file system
    # in real app - database like postgre sql - there it should be hidden in environment variable
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'


    # enabling sending emails to users - gmail setup from https://mailtrap.io/blog/flask-email-sending/

    # gmail disabled less secure apps in 2022 - NEW APPROACH
    # first turn on 2 factor authentification on gmail
    # then turn on 2step authentification, go to https://myaccount.google.com/apppasswords
    # generate password - 16 letters and use this to authenticate and put it into environment variables
    # restart PC and it should work
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # environment variables to hide sensitive data
    # control panel - system and security - system - advanced system settings - environment variables - new user variable
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')