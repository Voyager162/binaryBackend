from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource  # used for REST API building
import datetime as dt
from api.jwt_authorize import token_required
from model.binaryOverflowPost import BinaryOverflowPost

binaryOverflowPost_api = Blueprint('binaryOverflowPost_api', __name__, url_prefix='/api')

api = Api(binaryOverflowPost_api)

class BinaryOverflowPostAPI:
    class _CRUD(Resource):
        def get(self):
            posts = BinaryOverflowPost.query.all()
            json_ready = [post.read() for post in posts]
            return json_ready
        
        @token_required()
        def post(self):
            current_user = g.current_user
            data = request.get_json()
            current_date = dt.datetime.now()
            final_date = current_date.strftime
            post = BinaryOverflowPost(data["title"], data["post_ref"], current_user.id, final_date)
            return post
        
        @token_required()
        def put(self):
            current_user = g.current_user
            data = request.get_json()
            # Change from id, not a reliable one
            post = BinaryOverflowPost.query.get(data["id"])
            # WIP Feature, unknown if it works
            if post["_author"] == current_user.id:
                pass
            else:
                return "You cannot change another user's posts"
            
        @token_required()
        def delete(self):
            current_user = g.current_user
            data = request.get_json()
            post = BinaryOverflowPost.query.get(data["id"])
            if post["author"] == current_user.id:
                pass
            else:
                return "You cannot delete another user's posts"