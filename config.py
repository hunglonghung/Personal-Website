import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite://///Users/Admin/Desktop/My_workspace/WEBSITE/app/instance/app.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
