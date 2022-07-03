# TriviaAPI
A web application for playing the Trivia quiz game. 

![Trivia Home Page](./Screenshots/Trivia%20Home%20Page.jpg)

## Table of Contents

1. Project Motivation
2. Installations
3. File Descriptions
4. How to Interact with the Project

## Project Motivation:

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



