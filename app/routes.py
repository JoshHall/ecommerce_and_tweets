from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import TitleForm, PostForm, LoginForm, RegisterForm
from app.models import Post, User
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index')
@app.route('/index/<header>', methods=['GET'])
def index(header=''):
    products = {
        1001: {
            'title': 'Soap',
            'price': 3.98,
            'desc': 'Very clean soapy soap, descriptive text'
        },
        1002: {
            'title': 'Grapes',
            'price': 4.56,
            'desc': 'Bundle of grapey grapes, yummy'
        },
        1003: {
            'title': 'Pickles',
            'price': 5.67,
            'desc': 'A pickle a day keeps the goblins away'
        },
        1004: {
            'title': 'Juice',
            'price': 2.68,
            'desc': 'Yummy Yumy OJ Babyyyyy'
        }
    }
    return render_template('index.html', header=header, products=products, title='Home')


@login_required
@app.route('/posts/<username>',  methods=['GET','POST'])
def posts(username):
    form = PostForm()

    # query database for proper person
    person = User.query.filter_by(username=username).first()

    # when form is submitted append to posts list, re-render posts page
    if form.validate_on_submit():
        tweet = form.tweet.data
        post = Post(tweet=tweet, user_id=current_user.id)

        # add post variable to database stage, then commit
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts', username=username))

    return render_template('posts.html', person=person, title='Posts', form=form, username=username)

@app.route('/title', methods=['GET','POST'])
def title():
    form = TitleForm()

    # when form is submitted, redirect to home page and pass title to change what the h1 tag says
    if form.validate_on_submit():
        header = form.title.data
        return redirect(url_for('index', header=header))

    return render_template('title.html', title='Title', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user is logged in, do not let them access this page
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        # query the database for the user trying to login
        user = User.query.filter_by(username=form.username.data).first()

        # if user doesn't exist, reload page and flash messages
        if user is None or user.check_password(form.password.data):
            flash('Credentials are incorrect.')
            return redirect(url_for('login'))

        # if user does exist, and Credentials are correct, log them in and send them to their profile page
        login_user(user, remember=form.remember_me.data)
        flash('You are now logged in!')
        return redirect(url_for('posts', username=current_user.username))

    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # if user is logged in, do not let them access this page
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data,
            url = form.url.data,
            age = int(form.age.data),
            bio = form.bio.data
        )

        # set the password hash
        user.set_password(form.password.data)

        # add to stage and commit to db, then flash and return
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
