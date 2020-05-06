import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
## db_drop_and_create_all()

## ROUTES
'''
Done implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    drinks = [drink.short() for drink in drinks]
    return jsonify({
        "success": True,
        "drinks": drinks
    })


'''
Done implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_detail(jwt):

    drinks = Drink.query.all()
    drinks = [drink.long() for drink in drinks]
    print(drinks)
    return jsonify({
        "success": True,
        "drinks": drinks
    })


'''
done implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    drink = request.get_json()
    if drink is None:
        abort(404)
    title = drink['title']
    recipe = drink['recipe']
    try:
        print(title, recipe)
        drink = Drink(title=title, recipe=json.dumps(recipe))
        print(drink)
        drink.insert()
    except:
        abort(422)
    return (jsonify({
        "success": True,
        "drinks": drink.long()
        }))
    

'''
done implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(id):
    update = request.get_json()
    print(update)
    drink = Drink.query.get(id)
    if drink == None:
        abort(404)
    update_title = request.get_json()['title']
    update_recipe = json.dumps(request.get_json()['recipe'])
    if drink.title != update_title:
        drink.title = update_title
    if drink.recipe != update_recipe:
        drink.recipe = update_recipe
    try:
        drink.update()
    except:
        abort(422)
    drinks = [drink.title, drink.recipe]
    return jsonify({
        "success": True,
        "drinks": drinks
    })
'''
done implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id):
    drink = Drink.query.get(id)
    
    if drink == None:
        abort(404)
    
    drink.delete()
    
    return jsonify({
        "success": True,
        "delete": id
        })

    
    
## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
done implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
done implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "Resource not found."
    }), 404

'''
done implement error handler for AuthError
    error handler should conform to general task above 
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'error': error.error,
        'status_code': error.status_code
    }), '401'