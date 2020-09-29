import os

from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import datetime

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_validation" , methods=["POST", "GET"])
def login_validation():
    if request.method == 'POST':
        # get user info from input
        email = request.form['signinEmail']
        password = request.form['signinPassword']

        # check if password match with database
        check_user = db.execute("select * from public.users where email = :email", {'email' : email}).fetchone()

        if check_user:
            list = []
            for i in check_user:
               list.append(i)

            check_name = list[0]
            check_email = list[1]
            check_pass = list[2]
            check_date = list[3]
            if check_email == email and check_pass == password:
                session.permanent = True
                session['name'] = check_name
                session['password'] = check_pass
                session['email'] = check_email
                session['date'] = check_date
                flash('Signin successful')
                return redirect(url_for('home'))
            else:
                flash('User name or password is incorrect')
                return redirect(url_for('login'))
        else:
            flash('You have not account in this website. Please register first.')
            return redirect(url_for('login'))
    else:
        flash('Login Failed')
        return redirect(url_for('login'))


@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/registration_validation" , methods = ['POST','GET'])
def registration_validation():
   if request.method == 'POST':
      # get data from user inputs
      name = request.form['signupName']
      email = request.form['signupEmail']
      password = request.form['signupPassword']

      #check if the email is already in the table
      check_user = db.execute("select * from public.users where email = :email", {'email' : email}).fetchall()

      if check_user:
         flash('You are already registed.')
         return redirect(url_for('signin'))
      else :
         # add a new user in database
         db.execute("INSERT INTO public.users (name, email, password) VALUES (:name, :email , :password)", {
            "name":name, "email":email, "password":password})
         db.commit()

         #save the data in session
         session['name'] = name
         session['email'] = email
         session['password'] = password

         flash('Registraion successful')
         return redirect(url_for('home'))
   else:
      if 'name' in session:
         flash('You are Already registered ')
         return redirect(url_for('home'))
      else:
         return render_template('signin.html')


@app.route("/home")
def home():
	baseUrl = request.base_url
	list = []
	result = db.execute(" SELECT * FROM books ;").fetchall()
	#if found then save it in list
	if result:
		for i in result :
			list.append(i)
		return render_template('home.html', baseUrl = baseUrl,  items = list)

	#if not found show a not found message
	else:
		return render_template('home.html', msgNo = "Sorry! No books found" , text = "this account")



@app.route("/profile")
def profile():
	if 'email' in session:
		db_review_query = db.execute(" select * from public.reviews where email = :email", {'email' : session['email']}).fetchall()
		# user data
		userInfo = {
			'name': session['name'],
			'email': session['email'],
			'password': session['password'],
			'date': session['date']
		}
		reviewCount = len(db_review_query)

		return render_template('profile.html', userInfo = userInfo, reviewedbooks = db_review_query , reviewCount= reviewCount )

	else:
		flash('Login first')
		return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'name' in session:
        session.pop('name', None)
        session.pop('email', None)
        session.pop('password', None)

        flash('Logged out successfully', 'info')
        return redirect(url_for('login'))
    else:
        flash('Already Logged out')
        return  redirect(url_for('login'))


@app.route('/book', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        title = request.form['byTitle']
        title = title.title()
        author = request.form['byAuthor']
        year = request.form['byYear']
        isbn = request.form['byIsbn']

        list = []
        text = None
        baseUrl = request.base_url
        if title:
            result = db.execute(" SELECT * FROM books WHERE title LIKE '%"+title+"%' ;").fetchall()
            text = title
        elif author:
            result = db.execute(" SELECT * FROM books WHERE author LIKE '%"+author+"%' ;").fetchall()
            text = author
        elif year:
            result = db.execute(" SELECT * FROM books WHERE year = :year", {'year':year}).fetchall()
            text = year
        else:
            result = db.execute(" SELECT * FROM books WHERE isbn LIKE '%"+isbn+"%' ;").fetchall()
            text = isbn

        #if found then save it in list
        if result:
            for i in result :
                list.append(i)
            itemsCount = len(list)
            return render_template('home.html', baseUrl = baseUrl,  items = list, msg = "Search result found", text = text , itemsCount = itemsCount)

        #if not found show a not found message
        else:
            return render_template('home.html', msgNo = "Sorry! No books found" , text = text)



    return render_template ('home.html')
