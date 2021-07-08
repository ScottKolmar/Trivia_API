# Backend - Full Stack Trivia API 

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

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

### Getting Started
- Backend Base URL: http://127.0.0.1:5000/
- Frontend Base URL: http://127.0.0.1:3000/

### Endpoints

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a categories key that contains a object with key of category id and value of category type, and a success key.
- Example: ```curl http://127.0.0.1:5000/categories```
```
{
    "categories": {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
        },
        "success": True
}
```
#### POST '/categories'
- Creates a new category using the specified input information
- Request Arguments: An object with a key type containing a string of the category type, like the following:
```
{
    "type": "Orcs"
}
```
- Request Returns: An object with a created key containing the id of the created category, and a success key.
- Example: ```curl -X POST -H "Content-Type: application/json" -d '{"type": "Orcs"}' http://127.0.0.1:5000/categories```
```
{
    "created":7,
    "success":true
}
```
#### GET '/questions?page=${integer}'
- Fetches all the questions in the database, paginated with 10 questions per page.
- Request Arguments: page - integer
- Request Returns: An object with a categories key that contains a object with key of category id and value of category type, a questions key, which contains a list of questions, a total questions key, and a success key.
- Example: ```curl http://127.0.0.1:5000/questions```
```
{
    "categories":{
        "1":"Science",
        "2":"Art",
        "3":"Geography",
        "4":"History",
        "5":"Entertainment",
        "6":"Sports",
        "7":"Orcs"
        },
        "currentCategory":null,
        "questions":[
            {
                "answer":"Tom Cruise",
                "category":"5",
                "difficulty":4,
                "id":4,
                "question":
                "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
            },
            {
                "answer":"Maya Angelou",
                "category":"4",
                "difficulty":2,
                "id":5,
                "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            {
                "answer":"Edward Scissorhands",
                "category":"5",
                "difficulty":3,
                "id":6,
                "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            },
            {
                "answer":"Muhammad Ali",
                "category":"4",
                "difficulty":1,
                "id":9,
                "question":"What boxer's original name is Cassius Clay?"
            },
            {
                "answer":"Brazil",
                "category":"6",
                "difficulty":3,
                "id":10,
                "question":"Which is the only team to play in every soccer World Cup tournament?"
            },
            {
                "answer":"Uruguay",
                "category":"6",
                "difficulty":4,
                "id":11,
                "question":"Which country won the first ever soccer World Cup in 1930?"
            },
            {
                "answer":"George Washington Carver",
                "category":"4",
                "difficulty":2,
                "id":12,
                "question":"Who invented Peanut Butter?"
            },
            {
                "answer":"Lake Victoria",
                "category":"3",
                "difficulty":2,
                "id":13,
                "question":"What is the largest lake in Africa?"
            },
            {
                "answer":"The Palace of Versailles",
                "category":"3",
                "difficulty":3,
                "id":14,
                "question":"In which royal palace would you find the Hall of Mirrors?"
            },
            {
                "answer":"Agra",
                "category":"3",
                "difficulty":2,
                "id":15,
                "question":"The Taj Mahal is located in which Indian city?"
            }
            ],
            "success":true,
            "totalQuestions":10
} 
```
#### DELETE '/questions/int:id'
- Deletes the question specified by the id in the URL
- Request Arguments: None
- Request Returns: An object with a deleted key that indicates which question was deleted,and a success key.
- Example: ```curl -X DELETE http://127.0.0.1:5000/questions/5```
```
{
    "success": True,
    "deleted": 5
}
```
#### POST '/questions'
- Creates a new question. Each input field is required; if any input field contains None, the request will return Error 422.
- Request Arguments: A JSON object like the following:
```
{
    "question": "What is the meaning of life?",
    "answer": 42,
    "difficulty": 5,
    "category": 1
}
```
- Request Returns: An object with a success key, a created key that contains the id of the created question, and a total questions key.
- Example: ```curl -X POST -H "Content-Type: application/json" -d '{"question":"What is the meaning of life?","answer": 42,"difficulty": 5,"category": 1}' http://127.0.0.1:5000/questions```
```
{
    "success": True,
    "created": 11,
    "total_questions": 10
}
```
#### POST '/questions/' with search parameter
- Finds questions which match a provided search parameter (in the question key), case insensitive.
- Request Arguments: An object with a search key like the following:
```
{
    "search": "Warcraft"
}
```
- Request Returns: An object with a questions key containing a list of questions, a success key, and a total questions key.
- Example: ```curl -X POST -H "Content-Type: application/json" -d '{"search": "Warcraft"}' http://127.0.0.1:5000/questions```
```
{
    "questions":[],
    "success":true,
    "total questions":0
}
```
#### GET '/categories/int:id/questions'
- Retrieves questions from the specified category via the category id.
- Request Arguments: None
- Request Returns: An object with a current category key, a questions key that contains a list of questions, a success key, and a total questions key which contains the total number of questions in the category.
- Example: ```curl http://127.0.0.1:5000/categories/2/questions```
```
{
    "currentCategory":"Art",
    "questions":[
        {"answer":"Escher","category":"2","difficulty":1,
        "id":16,
        "question":"Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {
            "answer":"Mona Lisa","category":"2",
            "difficulty":3,
            "id":17,
            "question":"La Giaconda is better known as what?"
        },
        {
            "answer":"One",
            "category":"2",
            "difficulty":4,
            "id":18,
            "question":"How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer":"Jackson Pollock","category":"2",
            "difficulty":2,
            "id":19,
            "question":"Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        }
],
"success":true,
"totalQuestions":4
}
```
#### POST '/quizzes'
- Retrieves a question within a specified category that is not in a list of user specified previous questions.
- Request Arguments: An object with a category key containing both the category type as a string and a category id as a string and a previous questions key containing a list of previous question ids, like the following:
```
{
    "quiz_category": {
        "type": "Science",
        "id": "1",
    },
    "previous_questions": [1,6,7,8]
}
```
- Request Returns: An object with a question key containing a new question, and a success key.
- Example : ```curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [1,6,7,8], "quiz_category": {"type":"Science","id":"1"}}' http://127.0.0.1:5000/quizzes```
```
{
    "question":{
        "answer":"Blood",
        "category":"1",
        "difficulty":4,
        "id":22,
        "question":"Hematology is a branch of medicine involving the study of what?"
        },
        "success":true
}
```
### Error Handling
Errors are returned in the following json format:
```
{
    'success': False,
    'error': 404,
    'message': 'Resource Not Found'
}
```
The API returns 4 types of errors:
- 400: bad request
- 404: not found
- 422: unprocessable
- 500: internal server error

## Author Acknowledgement
- Scott Kolmar contributed to the backend via ```__init__.py```, the test file ```test_flaskr.py``` and this README.
- The project and other files were contributed by [Udacity](http://udacity.com)