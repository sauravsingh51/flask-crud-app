'''
This backend app exposes REST enpoints for performing various CRUD related operations.

This is the starter file, all the flask and db related imports/initialisations are done here.
All models for performing ORM mappings with db are present in the model class below.
All controllers having REST endpoints are present with @app.route decorator.
'''

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__) #initializing the Flask app

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') #initlizing db url (check docker-compose)

db = SQLAlchemy(app)

class AppInfoModel(db.Model):  # model class for mapping db table with attributes 
  id = db.Column(db.Integer, primary_key=True)
  app_name = db.Column(db.VARCHAR(80), unique=True, nullable=False)
  created_on = db.Column(db.TIMESTAMP, nullable=False)
  last_deployed_on = db.Column(db.TIMESTAMP, nullable=False)
  sonar_key =  db.Column(db.VARCHAR(80), unique=True, nullable=False)
  code_quality = db.Column(db.VARCHAR(5), nullable=False)
  code_coverage = db.Column(db.VARCHAR(5), nullable=False)
  is_active = db.Column(db.BOOLEAN, nullable=False)


  def __init__(self, app_name, created_on, last_deployed_on, sonar_key, code_quality, code_coverage, is_active):
    self.app_name = app_name
    self.created_on = created_on
    self.last_deployed_on = last_deployed_on
    self.sonar_key = sonar_key
    self.code_quality = code_quality
    self.code_coverage = code_coverage
    self.is_active = is_active


db.create_all() # creating the tables automatically (if they don't exist) based on the column definion given in models


# all the REST calls are mentioned below for CRUD operations

@app.route('/app', methods=['GET']) #GET call for fetching all the apps from db
def get_all_apps():
  apps = []
  for item in db.session.query(AppInfoModel).all():
    del item.__dict__['_sa_instance_state']
    apps.append(item.__dict__)
  return jsonify(apps), 200

@app.route('/app/<id>', methods=['GET']) #GET call for fetching a specific app from db using id
def get_app_by_id(id):
  app = AppInfoModel.query.get(id)
  del app.__dict__['_sa_instance_state']
  return jsonify(app.__dict__), 200

@app.route('/app', methods=['POST']) #POST call for creating/adding new apps to db
def create_app():
  body = request.get_json()
  app_name = body['app_name']
  created_on = body['created_on']
  last_deployed_on = body['last_deployed_on']
  sonar_key = body['sonar_key']
  code_quality = body['code_quality']
  code_coverage = body['code_coverage']
  is_active = body['is_active']
  db.session.add(AppInfoModel(app_name, created_on, last_deployed_on, sonar_key, code_quality, code_coverage, is_active))
  db.session.commit()
  return "App created", 201

@app.route('/app/<id>', methods=['PUT']) #PUT call for updating exisitng app by id 
def update_app_by_id(id):
  body = request.get_json()
  app_name = body['app_name']
  created_on = body['created_on']
  last_deployed_on = body['last_deployed_on']
  sonar_key = body['sonar_key']
  code_quality = body['code_quality']
  code_coverage = body['code_coverage']
  is_active = body['is_active']
  db.session.query(AppInfoModel).filter_by(id=id).update(
    dict(sonar_key=sonar_key, code_quality=code_quality))
  db.session.commit()
  return "App details updated", 200

@app.route('/app/<id>', methods=['DELETE']) #DELETE call for deleting app by id 
def delete_app_by_id(id):
  db.session.query(AppInfoModel).filter_by(id=id).delete() 
  
    #or just set the is_active flag to false for avoiding permanent delete
    #db.session.query(Item).filter_by(id=id).update(
    #dict(is_active=False))
    

    
    #if the above commented lines are used for deleting entries (updating the flag) then,
    #please add/change condition for GET functions (add contition for is_active=True)
    #otherwise it will fetch all the entries
    

  db.session.commit()
  return "App deleted", 204

if __name__ == '__main__':
    app.run(debug=True)





