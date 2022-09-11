from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = '@#$%$%$#$%^%78saj29873$%^&**'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/phongkham2?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

cloudinary.config(
    cloud_name='dfkf0cjct',
    api_key='566413819673345',
    api_secret='UsB2itfGSrg0kYyuaD-ZfR7u-tI'
)

login = LoginManager(app=app)

from twilio.rest import Client

account_sid = 'AC6bb2c7c082e3bd77300156ae6886c6bc'
auth_token = '64fab92e39456fd86db0db4043a8ae9d'
client = Client(account_sid, auth_token)


