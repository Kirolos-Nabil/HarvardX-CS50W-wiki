# Project 1

Course name: Web Programming with Python and JavaScript
Hint: I made this project to accomplish project1 portion of HarvardX CS50W course
Live link https://book-cafe.herokuapp.com/
App name: book-cafe

Breif description: This is a simple book review app made with flask. To use this website features you have to login first. Anyone can register in this website. After registration and logged into the website people can search for books, view reviews on particular book and can submit his own review.

Technology used: HTML, CSS, BOOTSTRAP, PYTHON, FLASK, SQLALCHEMY, POSTGRESQL

Book API used: goodreads.com (Thank you for free api)

Server used: heroku.com (Thank you for free web service)

Features:

Login: If user go to root url first it will check if the user is already signed in or not using the session. If not then app will show the login page otherwise app will take the user to the account page without asking him to login everytime. When login page apprears and user input his email and password - app will compare the informations with informations that are already saved in database. If the username and password match then user wiil be logged in and allowed to go to account page.

Registration: New user can register on the website. Before registration app will check if there is already any account registered with the same email. If no account found than app will register the account in the website.

Logout: Users can log out from the website by clicking on the logout button.

Home page: To view the home page user must log in first. In the home page users can see all books and search for books.

Search: By clicking the search menu button Users can search books by Title or Author or Year or ISBN number. If user submit the keyword in the search bar a search result will appear with book list with that information.

Book-Details page: By clicking a view details from the search result users can view information about that book. Information will come from goodread.com api and reviews data will come from my website database.

Api: https://book-cafe.herokuapp.com/cafe-books/api/ISBN Replace the ISBN with the real book's isbn number to get a book information in json format . User must be logged in use API endpoint
