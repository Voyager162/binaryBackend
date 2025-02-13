from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource  # used for REST API building
from api.jwt_authorize import token_required
from model.binaryOverflowComments import BinaryOverflowComments
from model.binaryOverflowContent import BinaryOverflowContent
from model.binaryOverflowContentVotes import BinaryOverflowContentVotes
from model.binaryOverflowCommentVotes import BinaryOverflowCommentVotes

binaryOverflow_api = Blueprint('binaryOverflow_api', __name__, url_prefix='/api')

api = Api(binaryOverflow_api)

class BinaryOverflowPostAPI:
    # Fetches data for Frontend to build
    class fetch_frontend(Resource):
        def get(self):
            posts = BinaryOverflowContent.query.all()
            json_ready = [post.read() for post in posts]
            return json_ready

    # CRUD for the content model
    class POST_CRUD(Resource):
        def get(self):
            post_id = request.args.get('id')
            try:
                post = BinaryOverflowContent.query.get(post_id)
                post_json_ready = post.read()
                comments = post.comments
                comments_json_ready = [comment.read() for comment in comments]
                return {
                    'post': post_json_ready,
                    'comments': comments_json_ready
                }
            except Exception as e:
                return "There was an issue with fetching the post: " + str(e)

        
        @token_required()
        def post(self):
            current_user = g.current_user
            data = request.get_json()
            post = BinaryOverflowContent(data["title"], data["post_ref"], current_user.id)
            post.create()
            return jsonify(post.read())
        
        @token_required()
        def put(self):
            current_user = g.current_user
            data = request.get_json()
            # Change from id, not a reliable one
            post = BinaryOverflowContent.query.get(data["id"])
            # WIP Feature, unknown if it works
            if post["_author"] == current_user.id:
                pass
            else:
                return "You cannot change another user's posts"
            
        @token_required()
        def delete(self):
            current_user = g.current_user
            data = request.get_json()
            # Change to reference post_id
            post = BinaryOverflowContent.query.get(data["id"])
            author = post.read()["author"]
            if author == current_user.id:
                post.delete()
                return "post sucessfully deleted"
            else:
                return "You cannot delete another user's posts"
            
    class CONTENT_VOTE(Resource):
        @token_required()
        def post(self):
            data = request.get_json()
            current_user = g.current_user
            vote = BinaryOverflowContentVotes.query.filter_by(_user=current_user.id, id=data['post_id']).first()
            if vote:
                vote.update(data)
            else:
                vote = BinaryOverflowContentVotes(data["post_id"], current_user.id, data["vote"])
                vote.create()
            return jsonify(vote.read())
        
    class COMMENT_VOTE(Resource):
        @token_required()
        def post(self):
            data = request.get_json()
            current_user = g.current_user
            vote = BinaryOverflowCommentVotes.query.filter_by(_user=current_user.id, id=data['post_id']).first()
            if vote:
                vote.update(data)
            else:
                vote = BinaryOverflowCommentVotes(data["post_id"], current_user.id, data["vote"])
                vote.create()
            return vote.read()
    
    api.add_resource(fetch_frontend, '/binaryOverflow/home')
    api.add_resource(POST_CRUD, '/binaryOverflow/post')
    api.add_resource(CONTENT_VOTE, '/binaryOverflow/contentVote')
    api.add_resource(COMMENT_VOTE, '/binaryOverflow/commentVote')