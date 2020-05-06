- [Table-Top Tournaments Organizer (TTTO)](#table-top-tournaments-organizer-ttto)
  - [Motivation for project](#motivation-for-project)
  - [Project dependencies](#project-dependencies)
    - [Python Requirements list:](#python-requirements-list)
  - [Local Development](#local-development)
    - [3rd Party Dependencies](#3rd-party-dependencies)
      - [Heroku CLI](#heroku-cli)
      - [PostgreSQL](#postgresql)
      - [Auth0](#auth0)
        - [Setting up Auth0](#setting-up-auth0)
        - [Permissions and Roles](#permissions-and-roles)
    - [Running server Locally](#running-server-locally)
  - [Hosting instructions](#hosting-instructions)
  - [API behavior and Permissions](#api-behavior-and-permissions)
    - [Endpoints](#endpoints)
      - [characters](#characters)
      - [groups](#groups)
    - [Methods](#methods)
    - [Example Requests and Responses](#example-requests-and-responses)
      - [`/characters` and `/groups` (Public)](#characters-and-groups-public)
        - [GET](#get)
      - [`/characters/(#)` (Player, Admin)](#characters-player-admin)
        - [POST](#post)
        - [PATCH](#patch)
        - [DELETE](#delete)
      - [`/group/(#)` (DM, Admin)](#group-dm-admin)
        - [POST](#post-1)
        - [PATCH](#patch-1)
        - [DELETE](#delete-1)
    - [Error Messages](#error-messages)
      - [422 Unprocessable](#422-unprocessable)
      - [404 Not Found](#404-not-found)
      - [401 Authorization Error](#401-authorization-error)
# Table-Top Tournaments Organizer (TTTO)
Sample URL: https://fsdn-capstone.herokuapp.com/
## Motivation for project
This api was created for Organizers for Table Top Tournaments (Yeah, they have those) This allows an organizer, Game Masters, players, and those interested in the games to quickly create, edit, and organize player groups and characters related to those groups. 
## Project dependencies
TTTO is written in Python and has a handful of dependencies to run out-of-the-box.
It's is strongly recommended that you work within a virtual environment while developing with this API.
Run these commands within your working directory:
```bash
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
```
The last command will activate the virtual environment. Anything installed with pip will remain active only when the source command is ran and the env is active. It can be deactivated by typing `deactivate`

After activating a virtual env, the application's requirements can be installed by running:
```bash 
pip install -r requirements.txt
```     
### Python Requirements list:
- alembic==1.4.2
- click==7.1.1
- ecdsa==0.15
- Flask==1.1.2
- Flask-Cors==3.0.8
- Flask-Migrate==2.5.3
- Flask-Script==2.0.6
- Flask-SQLAlchemy==2.4.1
- gunicorn==20.0.4
- itsdangerous==1.1.0
- Jinja2==2.11.1
- jose==1.0.0
- Mako==1.1.2
- MarkupSafe==1.1.1
- psycopg2-binary==2.8.5
- pyasn1==0.4.8
- python-dateutil==2.8.1
- python-editor==1.0.4
- python-jose==3.1.0
- rsa==4.0
- six==1.14.0
- SQLAlchemy==1.3.16
- Werkzeug==1.0.1
## Local Development
### 3rd Party Dependencies
#### Heroku CLI 
Heroku Requires that you install GIT and there are various ways to get GIT and Heroki CLI installed. Please refer to [Heroku documentation](https://devcenter.heroku.com/articles/getting-started-with-python) for more information.
#### PostgreSQL
PostgreSQL is the Database flavor of choice here. The ORM of choice is SQLAlchemy which will be installed with the rest of the requirements.txt file. You have the options two options for development, to install Postgres locally or install the add-on Postgres in Heroku ([more info here](https://devcenter.heroku.com/articles/getting-started-with-python#provision-a-database)).
Which ever route you go you will need to update the following line in the models.py file if you are using Heroku to host your database, the setting page on their website will give you the properly formatted URI:
```python
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://{username}:{password}@{domainOrLocation}:{port}/{dbName}'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
``` 
#### Auth0
This api uses Auth0 out of the box. A free profile can be obtained from: https://www.auth0.com and the following permissions and roles will need to be set up before running the API server.
##### Setting up Auth0
You will need to edit two items in the auth.py document so that you are able authenticate into your own Auth0 instances. The needed edits are are: AUTH0_DOMAIN and API_AUDIENCE. 
```python
AUTH0_DOMAIN = '{yourdomain}.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = '{yourAPITitle}'
```
##### Permissions and Roles

There are three(3) Roles currently set up they are the following:

1. **player**
   1. post:character
   2. patch:character
   3. delete:character
2. **dm**
   1. post:group
   2. patch:group
   3. delete:group
3. **admin**
   1. post:character
   2. patch:character
   3. delete:character
   4. post:group
   2. patch:group
   3. delete:group

### Running server Locally
A local server can be ran from the command line and from within the projects folder fun the following commands:
(**Note:** This readme assume that you are using a Unix based system. It's strongly advised to use "Windows Subsystem for Linux" if you are using a Windows based operating system)

```bash
export FLASK_APP=app
export FLASK_ENV=development
```
This will start the server with a webserver on http://localhost:5000 and you will be able to send requests to http://localhost/characters or http://localhost/groups

You can curl, or use applications like Postman to test endpoints.

There is also a Sample UI provided with this API that will also run on http://localhost:5000. If configured correctly you will be able to Add, Edit, and Delete Characters and Groups. You will need to update the Auth0 Login URL located on line 53 on the file /templates/base.html.

```javascript
const loginBtn = document.getElementById('login')
    if (sessionStorage.getItem('token') === null) {
        loginBtn.innerText = 'Login';
        loginBtn.onclick = function login() {
            window.location.href = 'YourLoginURL'; /*This Line needs to be altered to fit your Auth0 Login url*/
        };
    } else if (sessionStorage.getItem('token')) {
        loginBtn.innerText = 'Logout';
        loginBtn.onclick = function logout() {
            sessionStorage.clear();
            window.location.href = '/';
        };
    }
```

## Hosting instructions

This application is set up to be built and hosted on the service **[Heroku](https://www.heroku.com)** Please follow the Heroku documentation for creating a code pipeline between Heroku and your Git solution of choice.

## API behavior and Permissions
This API has two basic endpoints, `/characters` and `/groups` while both have a GET that is publicly available (not needing authentication), they both have Post, Patch, and Delete methods which are restricted to players (`/characters`) and dms (`/groups`) there is a third admin role which is able to use both endpoints fully.
### Endpoints
#### characters
- `/characters/` 
  - Standard end point to see all characters
- `/characters/#` 
  - This endpoint allows you to get specific characters  
    - Will also take Post, Patch, Delete methods
#### groups
- `/groups`
  - Standard end point to see all characters
- `/groups/#`
  - This endpoint allows you to get specific characters  
    - Will also take Post, Patch, Delete methods
### Methods
### Example Requests and Responses
**Note** All endpoints require Bearer Authorization Tokens in the request Headers.

**Example:** 
```
{
  'gender': gender,
  'job': job,
  'name': name,
  'player_name': player,
  'race': race
}),
headers: {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer tokenReturnedInCallback'
}
```
#### `/characters` and `/groups` (Public)
##### GET
**Request to `/characters`**

**Response**
```json
{
  "characters": [
    {
      "currency": "0",
      "gender": "male",
      "group": null,
      "id": 23,
      "job": "Wizard",
      "lvl": 1,
      "name": "Taako (from TV)",
      "player_name": "Justin",
      "race": "Elf"
    },
    {
      "currency": "0",
      "gender": "male",
      "group": null,
      "id": 24,
      "job": "Fighter/Rogue",
      "lvl": 1,
      "name": "Magnus Burnsides",
      "player_name": "Travis",
      "race": "Human"
    },
    {
      "currency": "0",
      "gender": "male",
      "group": null,
      "id": 25,
      "job": "Cleric",
      "lvl": 1,
      "name": "Merle Highchurch",
      "player_name": "Clint",
      "race": "Dwarf"
    }
  ],
  "success": true
}
```

**Request to `/characters/23`**

**Response**
```json
{
  "character": {
    "currency": "0",
    "gender": "male",
    "group": {
      "id": 10,
      "name": "Tres Horny Boys",
      "player_name": "Griffin"
    },
    "id": 23,
    "job": "Wizard",
    "lvl": 1,
    "name": "Taako (from TV)",
    "player_name": "Justin",
    "race": "Elf"
  },
  "success": true
}
```
**Request to `/groups`**

**Response**
```json
{
  "groups": [
    {
      "id": 10,
      "name": "Tres Horny Boys",
      "player_name": "Griffin"
    }
  ],
  "success": true
}
```
**Request to '/groups/10`**

**Response**

```json
{
  "characters": [
    {
      "id": 23,
      "job": "Wizard",
      "lvl": 1,
      "name": "Taako (from TV)"
    },
    {
      "id": 24,
      "job": "Fighter/Rogue",
      "lvl": 1,
      "name": "Magnus Burnsides"
    },
    {
      "id": 25,
      "job": "Cleric",
      "lvl": 1,
      "name": "Merle Highchurch"
    }
  ],
  "group": {
    "id": 10,
    "name": "Tres Horny Boys",
    "player_name": "Griffin"
  },
  "success": true
}
```
#### `/characters/(#)` (Player, Admin)
##### POST
**Request to `/characters`**
```json
{
    "gender": "male",
    "job": "Wizard",
    "name": "Taaco (from TV)",
    "player_name": "Justin",
    "race": "Elf"
  }
```
**Response**
```json
  {
  "character": {
    "currency": "0",
    "gender": "male",
    "group": null,
    "id": 23,
    "job": "Wizard",
    "lvl": 1,
    "name": "Taaco (from TV)",
    "player_name": "Justin",
    "race": "Elf"
  },
  "success": true
}
 ```
##### PATCH
**Request to `/characters/23`**
```json
{
    "currency": "0",
    "gender": "male",
    "group": null,
    "id": 23,
    "job": "Wizard",
    "lvl": 1,
    "name": "Taako (from TV)",
    "player_name": "Justin",
    "race": "Elf"
  }
```
**Response**
```json
{
  "character_id": 23,
  "success": true
}
```
##### DELETE 
**Request to `/characters/26`**
**Response**
```json
{
  "character_id": 26,
  "success": true
}
```
#### `/group/(#)` (DM, Admin)
##### POST
**Request to `/groups`**
```json
{
    "name": "Tres Horny Boys",
    "player_name": "Griffin"
 }
```
**Response**
```json
{
  "group": {
    "id": 10,
    "name": "Tres Horny Boys",
    "player_name": "Griffin"
  },
  "success": true
}
```
##### PATCH
**Request to `/groups/10`**
```json
{
  "characters": [
    {
      "id": 23
    },
    {
      "id": 24
    },
    {
      "id": 25
    }
  ],
  "group": {
    "id": 10,
    "master": {
      "player_name": "Griffin"
    },
    "name": "Tres Horny Boys"
  }
}
```
**Response**
```json
{
  "group_id": 10,
  "success": true
}
```
##### DELETE
**Request to `/groups/11`**
**Response**
```json
{
  "group_id": 11,
  "success": true
}
```
### Error Messages
Errors are returned in JSON format:
#### 422 Unprocessable
```json
{
    "success": False, 
    "error": 422,
    "message": "unprocessable"
}
```
#### 404 Not Found
```json
{
    "success": False,
    "error": 404,
    "message": "Resource not found."
}
```
#### 401 Authorization Error
This can have a handful of different error messages in a similar format all pertaining to Authentication and a Users Privileges:
```json
{
	"code": "authorization_header_missing",
	"description": "Authorization header is expected."
}

{
	"code": "invalid_header",
	"description": "Authorization header must start with 'Bearer'."
}

{
	"code": "invalid_header",
	"description": "Token not Found"
}

{
	"code": "invalid_header",
	"description": "Authorization header must be bearer token."
}

{
	"code": "invalid_claims",
	"description": "Permissions not included with JWT."
}

{
	"code": "unauthorized",
	"description": "Permission not found."
}

{
	"code": "invalid_header",
	"description": "Authorization malformed."
}

{
    "code": "token_expired",
    "description": "Token expired."
}

{
    "code": "invalid_header",
    "description": "Unable to parse authentication token."
}
```
