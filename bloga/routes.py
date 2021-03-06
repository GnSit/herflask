import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from bloga import app, db, bcrypt
from bloga.forms import RegForm, LoginForm, UpdateAccountForm
from bloga.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# posts = [
#     {
#     'author' : 'reda ghannam',
#     'title' : 'this is my first blog',
#     'content' : 'also the same content nothing else here',
#     'date_posted' : 'April 21, 2022'
#     },
#     {
#     'author' : 'reda',
#     'title' : 'this is my second blog',
#     'content' : 'also the same content nothing else here',
#     'date_posted' : 'April 21, 2019'
# } twetteri db
#     ]
posts=[]
@app.route('/')
@app.route('/home')
def home():
    image_file = url_for('static', filename='profile_pics/4bc57ef5258ff479.jpg')
    
    return render_template('index.html', posts=posts,image_file=image_file)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created , You can login now', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # checck if email in database
        user = User.query.filter_by(email=form.email.data).first()
        # if user found check password that it match with database 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Loggedin', 'info')
            return redirect(url_for('home'))
        #if we don't use mixin
        # if form.email.data == 'admin@blog.com' and form.password.data == 'pass':
        #     flash('You have been logged in!', 'success')
        #     return redirect(url_for('home'))
        # else:
        # end if we don't use mixin
        
        #else if wrong credentials
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)