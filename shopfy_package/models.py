from shopfy_package import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(25), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(100), nullable=False)
	profile = db.Column(db.String(25), default='default.jpg')
	products = db.relationship('Products', backref='seller',lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.profile}')"



class Products(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(25), nullable=False)
	product_category = db.Column(db.String(100), nullable=False)
	max_order = db.Column(db.Integer, nullable=False)
	one_piece = db.Column(db.Integer, nullable=False)
	free_shipping1 = db.Column(db.String(100), nullable=False)
	free_shipping2 = db.Column(db.String(100), nullable=False)
	product_description = db.Column(db.String(1000), nullable=False)
	product_image = db.Column(db.String(3000))
	product_image_name = db.Column(db.String(3000))
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
	seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Products('{self.product_name}','{self.date_created}', '{self.product_category}','{self.max_order}','{self.one_piece}', '{self.free_shipping1}', '{self.free_shipping2}',, '{self.product_image}')"



class Carts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, nullable=False)
	Carts_user = db.Column(db.String(234), nullable=False)

	def __repr__(self):
		return f"User('{self.product_id}','{self.Carts_user}')"

