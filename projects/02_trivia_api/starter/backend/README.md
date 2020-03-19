# Full Stack Trivia API Backend

- [Full Stack Trivia API Backend](#full-stack-trivia-api-backend)
  - [Getting Started](#getting-started)
  - [End Points:](#end-points)
    - [Method GET:](#method-get)
    - [Method DELETE:](#method-delete)
    - [Method POST:](#method-post)
  - [Request Example:](#request-example)
  - [Error Codes to Expect](#error-codes-to-expect)
    - [404 - Not Found](#404---not-found)
    - [422 - Unprocessable Entity](#422---unprocessable-entity)
    - [500 - Internal Server Error](#500---internal-server-error)
  - [Installing Dependencies](#installing-dependencies)
      - [Python 3.7](#python-37)
      - [Virtual Enviornment](#virtual-enviornment)
      - [PIP Dependencies](#pip-dependencies)
        - [Key Dependencies](#key-dependencies)
  - [Database Setup](#database-setup)
  - [Running the server](#running-the-server)
  - [Testing](#testing)

## Getting Started
This API does not require user accounts or authentication. Each request is sent and received in JSON format. The exact format is not all that different between the different API endpoints.


## End Points:
### Method GET:
1. /categories 
**Example:**
`curl -X GET http://localhost:5000/categories`
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```
2. /questions 
**Example:**
`curl -X GET  http://localhost:5000/questions?page=1`
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"        
    },
  ],
  "success": true,
  "total_questions": 1
}
```
3. /categories/<int:category_id>/questions 
**Example:**
`curl -X GET http://localhost:5000/categories/1/questions`
```json
{
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```
### Method DELETE:
1. /questions/<int:question_id> 
**Example:**
`curl -X DELETE http://localhost:5000/questions/20`
```json
{
  "deleted": 20,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```
### Method POST:
1. /questions
**Example:**
`curl -d '{"question":"How good is this?", "answer":"So Good", "difficulty":"1", "category":"5"}' -H "Content-Type: application/json" -X POST http://localhost:5000/questions`
```json
{
  "created": 37,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer":"So Good",
      "category":5,
      "difficulty":1,
      "id": 37,
      "question":"How good is this?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
2. /search
**Example:**
`curl -d '{"searchTerm":"Tom"}' -H "Content-Type: application/json" -X POST http://localhost:5000/search`
```json
{
  "currentCategory": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "totalQuestions": 2
}
```
3. /quizzes 
**Example:**
`curl -d '{"quiz_category":{"id":4,"type":"History"},"previous_questions": [1]}' -H 
"Content-Type: application/json" -X POST http://localhost:5000/quizzes`
```json
{
  "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  }
}
```
*Note, question will be equal to None when there are no more questions in that category*

## Request Example:
The /question endpoint will return a paginated response.

**Curl Request to get_questions:**

`curl -X GET  http://localhost:5000/questions?page=1`

**Response from the above request:**
``` json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"        
    },
  ],
  "success": true,
  "total_questions": 1
}
```

## Error Codes to Expect

### 404 - Not Found
This error is used when the server can't find the Category or Question requested
### 422 - Unprocessable Entity
This error is used when the server can't process your provided json
### 500 - Internal Server Error
This error is used when the server runs into an error

## Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```