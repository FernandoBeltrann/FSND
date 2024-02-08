# Build basic app

### File structure for a flask app

```bash
├── flaskr/
│   ├── __init__.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
└── .venv/
```

### Migrations
#### Set up

In the app file this should be present:

```bash
from flask_migrate import Migrate

migrate = Migrate(app,db)

```

The app and db should be instanced before, like in this snip code:

```bash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_URI

migrate = Migrate(app,db)

```

#### Terminal commands

First install Flask-Migrate as follows if this library is not already installed in the `requirements.txt ` file

```bash
pip install Flask-Migrate
```

In your terminal locate yourself in the directory where the app file is located and then execute the following commands: 

```bash
flask db init
```

This should create a folder with the name `migrations` where all the versions should get stored, it is important to excecute this command when located in the same file as the app, if not this will not work. 

This command will also create the columns of the tables and restrictions of them if already set in the `models` file.

After making changes in the schema run this command to make a provisional change in the schema:
```bash
flask db migrate
```

Finally if you are satisfied with the changes you can run the following command to apply the changes:
```bash
flask db upgrade
```

If something did not work and want to make a `Ctrl + Z` to your schema you can always run the following command as many times back as you would like to go back versions:
```bash
flask db downgrade
```


#### More
More detail and documentation here:
https://flask-migrate.readthedocs.io/en/latest/

The main documentations site for Alembic with complete references for everything:
https://alembic.sqlalchemy.org/en/latest/

### CORS
CORS 

First install the flask-cors library
```bash
pip install flask-cors

```

In the app you should import the CORS library and instance it in the `create_app` method :
```bash
from flask import
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route("/")
    @cross_origin()
    def helloWorld():
        return "Hello, cross-origin-world!"


return app

```
`@app.after_request` means that the app should run this after the app is runned.

`response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')`: state that 2 things will be allowed, in the header we will allow content and authorization.

`response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')`: states what methods you plan to allow.

`@cross_origin()`: when we add this it will apply the CORS to only the methods that have this instruction 

#### More
https://flask-cors.readthedocs.io/en/latest/#


### Test the API enpoints (CURL)

Use the CURL commands to test out in terminal the expected return of API

```bash
curl -X GET https://restcountries.com/v3.1/currency/cop

```

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/v1.0/categories'
GET ...
POST ...
DELETE ...

GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
