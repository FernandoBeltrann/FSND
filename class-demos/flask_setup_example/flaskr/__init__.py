import os
from flask_migrate import Migrate
from flask import Flask, abort, jsonify, Response, request
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Plant
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    #CORS(app, resources={r"*/api/*": {origins: '*'}}) This is when you want to allow only specific resources and origins to access
    CORS(app)

#Creating and configuring an app when having staging and production enviroment
    #app = Flask(__name__, instance_relative_config=True) # this means that there will be some config files in the project directory relative to the instance
    #app.config.from_mapping(
    #    SECRET_KEY='dev',
    #    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    #)
    #if test_config is None:
    #   this loads the configuration from config.py file, if it exists, when not testing
    #   app.config.from_pyfile('config.py', silent=True)
#END (config)



    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
        

    @app.route('/plants', methods=['GET', 'POST'])
    #def get_plants():
    #    plants = Plant.query.all()
    #    formatted_plants = [plant.format() for plant in plants]

    #    return jsonify({
    #        'success': True,
    #        'plants': formatted_plants        
    #    })
    
    #    return jsonify(plants=formatted_plants)
    
    def get_plants():
        plants = Plant.query.all()
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        formatted_plants = [plant.format() for plant in plants]
        response_json = json.dumps({
            'success': True,
            'plants': formatted_plants[start:end],
            'total_plants': len(formatted_plants)   
        }, indent=2)  # Sets the indentation level to 2 spaces
        return Response(response_json, mimetype='application/json')
    
    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id):
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

        if plant is None:
            abort(404)
        else:
            return jsonify({
                'success':True,
                'plant': plant.format()
            })

        
    @app.route('/smiley')
    #@cross_origin() Enable CORS on a single endpoint
    def smiley():
        return ':)'

    return app