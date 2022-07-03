# TriviaAPI
A web application for playing the Trivia quiz game. 

![Trivia Home Page](./Screenshots/Trivia%20Home%20Page.jpg)

## Table of Contents

1. About the Project
2. Installations
3. File Descriptions
4. How to Interact with the Project

## About the Project:

Trivia is a simple general knowledge game that anyone can play. This game can allow anyone to add any questions with the corresponding answers. It can retrieve these questions based on different categories. 

By clicking on play game, the application will return a set of random questions from a particular category. The user will be able to answer the question and will receive a point for every corect answer. The points will be tallied up and a final score will be displayed.

![Trivia Play](./Screenshots/Trivia%20Play.jpg)

## Installations:
The following libraries are required for the project: 
- Click
- Flask
- Flask-Cors
- Flask-RESTful
- Flask-SQLAlchemy
- itsdangerous
- Jinja2
- MarkupSafe
- psycopg2-binary
- python-dotenv
- SQLAlchemy

## File Descriptions

## How to Interact with the Project

In order for the application to run successfully, there are a number of steps that need to be followed. Run the following commands in a Linux terminal:

### Step 1
To start Postgres and set up the database:
```
bash setup-trivia.sh
```

### Step 2
Move into the backend directory and run the pip install for the requirements.txt file:
```
cd backend
pip3 install -r requirements.txt
```

### Step 3 
Start the backend server:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Step 4 
Navigate into the frontend directory and install libraries:
```
cd frontend
npm install
```

### Step 5 
Start the frontend server:
```
npm start
```



