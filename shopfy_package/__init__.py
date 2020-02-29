import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#engine = create_engine('sqlite:///C:Users\\ricky\\Desktop\\shopfy\\shopfy_package\\azizishop.db')

file_path = os.path.abspath(os.getcwd())+"\\azizishop.db"

UPLOAD_FOLDER = 'C:\\Users\\ricky\\Desktop\\shopfy\\shopfy_package\\static\\products_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b4a3e92b08b67e1369eb4ef91d40649c7a0620dd69b984d62d5b1f5f923c08158d4ddd12d1b4ada'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['SQLALCHEMY_DATABASE_URI'] = engine
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ file_path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///azizishop.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from shopfy_package import routes





