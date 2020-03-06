from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length ,Email, EqualTo, ValidationError
from shopfy_package.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])
	confirm_password = PasswordField('confirm_password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign Up')


	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("That username already taken. Please choose another username")

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("That Email already taken. Please choose another Email")		

		

class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired(),Length(min=8,max=20)])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')



class SettingForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Update setting')


	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("That username already taken. Please choose another username")

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("That Email already taken. Please choose another Email")	




class ProductForm(FlaskForm):
	product_name = StringField('product name',validators=[DataRequired()])
	product_category = SelectField('product product category',choices = [
						('1','All department'),
		                	('2','Art and Craft'),
		                		('3','Automotive'),
                       				 ('4','Baby'),
                        				('5','Beauty and personal Care'),
                        					('6','Book'),
                       							 ('7','Computer'),
                       								 ('8','Electronics'),
                       									 ('9','Home applience'),
                       										 ('10','Digital Music'),
                       											 ('11',"Men's fashion"),
                        											('12',"Women Fashion"),
                        												('13','Home and kitchen'),
                      														  ('14',"Boy's Fashion"),
                       															 ('15',"Girls Fashion"),
                       																 ('16',"Sports")],validators=[DataRequired()])
	max_order = IntegerField('Maximum order',validators=[DataRequired()])
	one_piece = IntegerField('One piece',validators=[DataRequired()])
	free_shipping1 = StringField('free shiping1',validators=[DataRequired()])
	free_shipping2 = StringField('free_shipping2',validators=[DataRequired()])
	product_image = FileField('Select product picture', validators=[FileAllowed(['png', 'jpg', 'jpeg', 'gif'])])
	product_description = TextAreaField('Write product description',validators=[DataRequired()])
	submit = SubmitField('Upload product')



class Update_productForm(FlaskForm):
	product_name = StringField('product name',validators=[DataRequired()])
	product_category = SelectField('product product category',choices = [
						('1','All department'),
		                	('2','Art and Craft'),
		                		('3','Automotive'),
                       				 ('4','Baby'),
                        				('5','Beauty and personal Care'),
                        					('6','Book'),
                       							 ('7','Computer'),
                       								 ('8','Electronics'),
                       									 ('9','Home applience'),
                       										 ('10','Digital Music'),
                       											 ('11',"Men's fashion"),
                        											('12',"Women Fashion"),
                        												('13','Home and kitchen'),
                      														  ('14',"Boy's Fashion"),
                       															 ('15',"Girls Fashion"),
                       																 ('16',"Sports")],validators=[DataRequired()])
	max_order = IntegerField('Maximum order',validators=[DataRequired()])
	one_piece = IntegerField('One piece',validators=[DataRequired()])
	free_shipping1 = StringField('free shiping1',validators=[DataRequired()])
	free_shipping2 = StringField('free_shipping2',validators=[DataRequired()])
	product_image = FileField('Select product picture', validators=[FileAllowed(['png', 'jpg', 'jpeg', 'gif'])])
	product_description = TextAreaField('Write product  description',validators=[DataRequired()])
	submit = SubmitField('Update product')
