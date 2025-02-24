from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource  # used for REST API building
from api.jwt_authorize import token_required
from model.leaderboard import Leaderboard
from model.user import User

"""
This Blueprint object is used to define APIs for the Post model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
leaderboard_api = Blueprint('leaderboard_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(leaderboard_api)

class LeaderboardAPI:
    """
    Define the API CRUD endpoints for the Post model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new post
    - get: read posts
    - put: update a post
    - delete: delete a post
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            # Obtain the current user from the token
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new post object using the data from the request
            post = Leaderboard(data['username'], current_user.id, data['average_score'])
            format= "%Y-%m-%d %H:%M:%S"
            # Save the post object using the ORM method defined in the model
            post.create()

            return jsonify(post.read())

        def get(self):
            # To read posts from user 
            
            # Find all the posts by the current user
            posts = Leaderboard.query.all()
            # Prepare a JSON list of all the posts, uses for loop shortcut called list comprehension
            json_ready = [post.read() for post in posts]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)
        
        def put(self):
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = Leaderboard.query.get(data['id'])
            # Update the post using the ORM method defined in the model
            post.update(data)
            # Return response
            return jsonify(post.read())
        
        @token_required()
        def delete(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = Leaderboard.query.get(data['id'])
            # Delete the post using the ORM method defined in the model
            post.delete()
            # Return response
            return jsonify({"message": "Post deleted"})

    """
    Map the _CRUD class to the API endpoints for /post.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
    api.add_resource(_CRUD, '/leaderboard')