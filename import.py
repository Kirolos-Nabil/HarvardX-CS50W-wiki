import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#Creat users table
db.execute(""" CREATE TABLE users (
    name varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    password varchar(100) NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (email));  """)

print('users table created')

#Creat books table
db.execute(""" CREATE TABLE books (
    id SERIAL NOT NULL,
    isbn varchar(100) NOT NULL,
    title varchar (100) NOT NULL,
    author varchar(100) NOT NULL,
    year integer NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (isbn) )  """)

print('books table created')

#Creat reviews table
db.execute(""" CREATE TABLE reviews (
    email varchar(100) NOT NULL,
    rating integer NOT NULL,
    comment varchar(1500) NOT NULL,
    isbn varchar(100) NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE) ;  """)

print('reviews table created')

#Insert books values
f = open('books.csv')
reader = csv.reader(f)

i = 1
for isbn, title, author, year in reader:

    i += 1

    if title == 'title':
        print ('1st row skipped')
    else:
        db.execute(" INSERT INTO public.books (isbn, title, author, year ) VALUES (:a, :b, :c, :d)", {'a':isbn, 'b':title, 'c': author, 'd':year} )
        print ( f"{i} books added successfully")

db.commit()
