import os
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from flask_cors import CORS
import json
import requests

from models import setup_db, Character, Group, db
from auth import requires_auth, AuthError

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)
  setup_db(app)

  return app

app=create_app()
#DONE: Get All Characters
  #Done Roles: Player, DM
@app.route('/characters', methods=['GET'])
def get_characters():
  characters = Character.query.all()
  toons = [character.full() for character in characters]
  return jsonify({
      "success": True,
      "characters": toons
  })

#DONE: Get Specific Character
@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
  character = Character.query.filter_by(id=character_id).first()
  if character is None:
    abort(404)

  return jsonify({
    "success": True,
    "character": character.full()
  })
  
#DONE: Get Groups 
  #Done Roles: Player, DM
@app.route('/groups', methods=['GET'])
def get_groups():
  groups = Group.query.all()
  parties = [group.full() for group in groups]
 
  return jsonify({
    'success': True,
    'groups': parties
  })

#DONE: Get Specific Group
  #Done Roles: Player, DM
@app.route('/groups/<int:group_id>', methods=['GET'])
def get_group_by_id(group_id):
  group = Group.query.get(group_id)
  if group is None:
    abort(404)
  members = group.characters
  characters = [member.short() for member in members]
  return jsonify({
    'success': True,
    "characters": characters,
    'group': group.full()
  })

#Done: Patch Characters 
  #Done Roles: Player
@app.route('/characters/<int:character_id>', methods=['PATCH'])
@requires_auth('patch:character')
def patch_character_by_id(jwt, character_id):
  character = Character.query.filter_by(id=character_id).first()
  if character == None:
    abort(404)
  update = request.get_json()
  if update == None:
    abort(422)
  player = update['player_name']
  name = update['name']
  race = update['race']
  job = update['job']
  gender = update['gender']
  lvl = update['lvl']
  currency = update['currency']
  character.player_name = player
  character.name = name
  character.race = race.capitalize()
  character.job = job.capitalize()
  character.gender = gender.lower()
  character.lvl = lvl
  character.currency = currency
  try:
    character.update()
  except:
    abort(422)
  finally:
    db.session.close()

  return jsonify({
    'success': True,
    'character_id': character_id 
  })


#Done: Patch Groups 
  #Done Roles: DM
@app.route('/groups/<int:group_id>', methods=['PATCH'])
@requires_auth('patch:group')
def patch_group(jwt, group_id):
  group = Group.query.get(group_id)
  print(group)
  if group == None:
    abort(404)
  update = request.get_json()
  print(update)
  if update == None:
    abort(422)
  characters = update['characters']
  group_update = update['group']
  master = group_update['master']
  player_name = master['player_name']
  name = group_update['name']
  character_id_list = []
  try:
    group.name = name
    group.master = player_name
    for c in characters:
      character_id_list.append(c['id'])
    if character_id_list is None:
      abort(404)
    character_list = Character.query.filter(Character.id.in_(character_id_list)).all()
    if character_list is None:
      abort(404)
    group.characters.clear()
    group.characters.extend(character_list)
    group.update()
  except:
    abort(422)
  finally:
    db.session.close()

  return jsonify({
    'success': True,
    'group_id': group_id 
  })
#Done: Delete Characters 
  #Done Roles: Player
@app.route('/characters/<int:character_id>', methods=['DELETE'])
@requires_auth('delete:character')
def delete_character(jwt, character_id):
  character = Character.query.filter_by(id=character_id).first()
  if character is None:
    abort(404)
  character.delete()

  return jsonify({
    'success': True,
    'character_id': character_id
  })
#Done: Delete Groups 
  #Done Roles: DM
@app.route('/groups/<int:group_id>', methods=['DELETE'])
@requires_auth('delete:group')
def delete_groups(jwt, group_id):
  group = Group.query.filter_by(id=group_id).first()
  if group is None:
    abort(404)
  group.delete()
  
  return jsonify({
    'success': True,
    'group_id': group_id
  })

#Done: Post Characters (note, error arose with pre-inserted content. was unable to insert until passing pre-existing PK values)
  #Done Roles: Player
@app.route('/characters', methods=['POST'])
@requires_auth('post:character')
def post_character(jwt):
  character = request.get_json()
  player_name = character['player_name']
  gender = character['gender'].lower()
  job = character['job']
  name = character['name']
  race = character['race']
  lvl = 1
  currency = str(0)
  try:
    character = Character(player_name=player_name, name=name, race=race, gender=gender, job=job, lvl=lvl, currency=currency)
    character.insert()
  except:
    abort(422)
  return jsonify({
    'success': True,
    'character': character.full()
  })

#Done: Post Groups 
  #Done Roles: DM
@app.route('/groups', methods=['POST'])
@requires_auth('post:group')
def post_group(jwt):
  group = request.get_json()
  name = group['name']
  player_name = group['player_name']
  try:
    group = Group(name=name, player_name=player_name)
    group.insert()
  except:
    abort(422)
  return jsonify({
    'success': True,
    'group': group.full()
  })

#UI Endpoints
URL = 'https://fsdn-capstone.herokuapp.com/'
@app.route('/')
def index():

  return render_template('index.html')

@app.route('/callback')
def callback():
  
  return redirect('/')

@app.route('/character')
def characters():
  characters = requests.get(URL + "/characters")
  return render_template('characters.html', characters=characters.json())

@app.route('/character/edit/<string:id>')
def edit_characters(id):
  character = requests.get(URL + "/characters/" + id)
  return render_template('characterEdit.html', character=character.json())

@app.route('/group')
def groups():
  groups = requests.get(URL + "/groups")
  return render_template('groups.html', groups=groups.json())

@app.route('/group/edit/<string:id>')
def edit_groups(id):
  group = requests.get(URL + "/groups/" + id)
  characters = requests.get(URL + "/characters")
  return render_template('groupEdit.html', group=group.json(),  addCharacters=characters.json())

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
  }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "Resource not found."
    }), 404

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        'error': error.error,
        'status_code': error.status_code
    }), '401'