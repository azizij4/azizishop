import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request, abort
from shopfy_package import app, db, bcrypt
from shopfy_package import  ALLOWED_EXTENSIONS ,UPLOAD_FOLDER 
from shopfy_package.forms import RegistrationForm, LoginForm, SettingForm, ProductForm, Update_productForm
from shopfy_package.models import User, Products, Carts
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/home')
def home():
	page = request.args.get('page',1, type=int)
	product=Products.query.order_by(Products.id.desc()).paginate(page=page, per_page=8)
	slide_1 = url_for("static", filename="slides/Slide4.png")
	slide_2 = url_for("static", filename="slides/slide5.jpeg")
	slide_3 = url_for("static", filename="slides/Apple-slider.jpg")
	slide_4 = url_for("static", filename="slides/appleiphone11banner.jpg")
	slide_5 = url_for("static", filename="slides/PayTM-offer.jpg")
	slide_6 = url_for("static", filename="slides/iphone.png")
	return render_template('home2.html',title = 'home',product=product,slide_6=slide_6,
										slide_3=slide_3,slide_2=slide_2,slide_1=slide_1,slide_4=slide_4,slide_5=slide_5)

@app.route('/register',methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f"{form.username.data} your account is successfull created. Your now able to log in",'success')
		
		return redirect(url_for('login'))


	return render_template("register.html",title='register',form=form)



@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):	
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			flash(f"Successfull logged in",'success')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash(f"Unsuccessfull loggin! Please check email and password",'danger')	
	return render_template("login.html",title= 'login',form=form)



@app.route('/logout')
def logout():
	logout_user()
	flash(f"successfull logout!",'success')
	#flash(f"It is better to login so that you can see more feature please try to login",'info')
	return redirect(url_for('home'))



@app.route('/wallet',methods=['GET','POST'])
@login_required
def wallet():
	return render_template('wallet.html',title='Wallet')




@app.route('/message',methods=['GET','POST'])
@login_required
def message():
	return render_template('message.html',title='message')




@app.route('/carts',methods=['GET','POST'])
@login_required
def carts():

	profile = url_for("static", filename="Users_profiles/" + current_user.profile)
	return render_template('carts.html',title='carts',profile=profile)


#fuction for save picture
def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/Users_profiles', picture_fn)
	#resizing image file to 130px 130px
	#output_size = (130, 130)
	#i = Image.open(form_picture)
	#i.thumbnail(output_size)
	#i.save(picture_path)
	form_picture.save(picture_path)

	return picture_fn

@app.route('/Account_setting',methods=['GET','POST'])
@login_required
def Account_setting():
	form = SettingForm()
	if form.validate_on_submit():
		#update user profile picture
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.profile = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash(f'Your account is successfull updated!','success')
		return redirect(url_for('Account_setting'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email	
	profile = url_for("static", filename="Users_profiles/" + current_user.profile)
	#profile = url_for("static", filename="Users_profiles/default.jpg")
	return render_template('Account_setting.html',title='setting' ,profile=profile,form=form)


@app.route('/to_seller',methods=['GET','POST'])
@login_required
def to_seller():
	product=Products.query.order_by(Products.id.desc())
	computer = url_for("static", filename="computer/71GbO41HbYL._SL1500_.jpg")
	profile = url_for("static", filename="Users_profiles/" + current_user.profile)
	return render_template('to_seller.html',title='seller', profile=profile,product=product,
																		computer=computer)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

	

@app.route('/create_product',methods=['GET','POST'])
@login_required
def create_product():
	form = ProductForm()
	if form.validate_on_submit():
		product_image=form.product_image.data
		if product_image and allowed_file(product_image.filename):
			filename = secure_filename(product_image.filename)
			#chage file image name to token hash 
			random_hex = secrets.token_hex(8)
			_, f_ext = os.path.splitext(product_image.filename)
			filename = random_hex + f_ext
			#save picture to file system
			product_image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		#add product from form to database	
		products = Products(product_name=form.product_name.data,
			product_category=form.product_category.data,
				max_order=form.max_order.data,
					one_piece=form.one_piece.data,
						free_shipping1=form.free_shipping1.data,
							free_shipping2=form.free_shipping2.data,
								product_description=form.product_description.data,
								    product_image_name=filename,
								      seller= current_user,
								      product_image=os.path.join(app.config['UPLOAD_FOLDER'],filename))
									
		db.session.add(products)
		db.session.commit()
		flash(f"Your product successfull created and posted",'success')
		return redirect(url_for('my_shop',username=current_user.username))
	#profile = url_for("static", filename="Users_profiles/default.jpg")
	profile = url_for("static", filename="Users_profiles/" + current_user.profile)
	return render_template('create_product.html',title='Create Product', form=form,profile=profile)


@app.route('/Admin')
@login_required
def Admin():
	users = User.query.all()
	profile = url_for("static", filename="Users_profiles/default.jpg")
	return render_template('Admin.html',users=users,profile=profile)

@app.route('/products/<int:Products_id>/<string:username>')
@login_required
def products(Products_id,username):
	profile = url_for("static", filename="Users_profiles/ + current_user.profile")
	product = Products.query.get_or_404(Products_id)

	user = User.query.filter_by(username=username).first_or_404()
	seller_product = Products.query.filter_by(seller=user).order_by(Products.id.desc())
	return render_template('products.html',product=product,title=product.product_name,
											profile=profile,seller_product=seller_product,user=user)

@app.route('/my_shop/<string:username>',methods=['GET','POST'])
@login_required
def my_shop(username):
	user = User.query.filter_by(username=username).first_or_404()
	product = Products.query.filter_by(seller=user).order_by(Products.id.desc()).paginate()
	if username != current_user.username:
		abort(403)
	if product is None:
		flash(f"You don't have any product start create ",'info')
	profile = url_for("static", filename="Users_profiles/" + user.profile)
	computer = url_for("static", filename="computer/71GbO41HbYL._SL1500_.jpg")
	#profile = url_for("static", filename="Users_profiles/default.jpg")
	return render_template('my_shop.html',title=current_user.username,user=user,username=username, profile=profile,
		                                                       product=product,computer=computer)

@app.route('/Seller/<string:username>')
@login_required
def user_products(username):
	#profile = url_for("static", filename="Users_profiles/ + u")
	user = User.query.filter_by(username=username).first_or_404()
	
	product = Products.query.filter_by(seller=user).order_by(Products.id.desc())
	profile = url_for("static", filename="Users_profiles/ + product.seller_id.profile")
	return render_template('seller_products.html',product=product,
		                   title=username,profile=profile,user=user)




@app.route('/my_shop/<string:username>/<int:Products_id>/Update_product', methods=['GET','POST'])
@login_required
def Update_product(username,Products_id):
	product = Products.query.get_or_404(Products_id)
	if username != current_user.username:
		abort(403)
	form = Update_productForm()
	if form.validate_on_submit():
		product_image=form.product_image.data
		if product_image and allowed_file(product_image.filename):
			filename = secure_filename(product_image.filename)
			#chage file image name to token hash 
			random_hex = secrets.token_hex(8)
			_, f_ext = os.path.splitext(product_image.filename)
			filename = random_hex + f_ext
			#save picture to file system
			product_image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		#update product to database	
		product.product_name=form.product_name.data
		product.product_category=form.product_category.data
		product.max_order=form.max_order.data
		product.one_piece=form.one_piece.data
		product.free_shipping1=form.free_shipping1.data
		product.free_shipping2=form.free_shipping2.data
		product.product_description=form.product_description.data
		product.product_image_name=filename
		product.seller= current_user
		product.product_image=os.path.join(app.config['UPLOAD_FOLDER'],filename)
		#commit new product details to a database
		db.session.commit()
		flash(f"Your product successfull updated", 'success')
		return redirect(url_for('my_shop',username=current_user.username))
	#populate last details to update product form	
	if request.method == "GET":
		form.product_name.data = product.product_name
		form.product_category.data = product.product_category
		form.max_order.data = product.max_order
		form.one_piece.data = product.one_piece
		form.free_shipping1.data = product.free_shipping1
		form.free_shipping2.data = product.free_shipping2
		form.product_description.data = product.product_description	
		
	return render_template('Update_product.html',product=product, form=form)

#function to delete product image in our file system
def Delete_product_image(product_image):
	product_image.delete(os.path.join(app.config['UPLOAD_FOLDER'],filename))




@app.route('/my_shop/<string:username>/<int:Products_id>/Delete_product', methods=['GET','POST'])
@login_required
def Delete_product(username,Products_id):
	product = Products.query.get_or_404(Products_id)
	if username != current_user.username:
		abort(403)
	db.session.delete(product)
	db.session.commit()
	flash(f"Your product is successfull deleted ", 'success')
	#return redirect(url_for('my_shop', username=current_user.username,Products_id=product.id))
	return redirect(request.referrer)


@app.route('/products/<int:Products_id>/Add_to_cart', methods=['GET','POST'])
@login_required
def Add_to_cart(Products_id):
	product = Products.query.get_or_404(Products_id)
	if request.method == 'POST':
		product_id = Carts(product_id=Products_id,Carts_user=current_user.username)
		db.session.add(product_id)
		db.session.commit()

	flash(f"Product successfull added to your cart", 'success')
	return redirect(request.referrer)



@app.route('/my_carts/<string:username>', methods=['GET','POST'])
@login_required
def my_carts(username):
	 carts = Carts.query.get_or_404(Carts_user=username)
	 if username != current_user.username:
	 	abort(403)
	 return render_template('my_carts.html',username=current_user.username)
