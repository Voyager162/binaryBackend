from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from __init__ import app
from model.binaryConverter import BinaryConverter

binary_converter_api = Blueprint('binary_converter_api', __name__, url_prefix='/api')

api = Api(binary_converter_api)  # Attach Flask-RESTful API to the Blueprint

class BinaryConverterAPI:
    """
    Define the API CRUD endpoints for the BinaryConverter model.
    """
    class _CRUD(Resource):
        def get(self):
            try:
                # Query all entries in the BinaryConverter table
                entries = BinaryConverter.query.all()
                # Convert the entries to a list of dictionaries using list comprehension
                results = [entry.read() for entry in entries]
                # Return the list of results in JSON format
                return jsonify(results)
            except Exception as e:
                # Return an error message in case of failure
                return jsonify({"error": str(e)}), 500

        def post(self):
            try:
                # Obtain the request data sent by the RESTful client API
                data = request.get_json()
                # Create a new BinaryConverter object using the data from the request
                post = BinaryConverter(data['binary'], data['decimal'])
                # Save the post object using the ORM method defined in the model
                post.create()
                # Return response to the client in JSON format
                return jsonify(post.read()), 201  # Added a 201 status code for successful creation
            except Exception as e:
                # Return an error message in case of failure
                return jsonify({"error": str(e)}), 500

        def put(self):
            try:
                # Obtain the request data
                data = request.get_json()
                # Find the BinaryConverter entry from the database
                post = BinaryConverter.query.get(data['id'])
                if not post:
                    return jsonify({"error": "Post not found"}), 404
                # Update the post
                post.binary = data['binary']  # Update the correct attribute
                post.decimal = data['decimal']  # Update the correct attribute
                # Save the changes
                post.update()
                # Return the updated post
                return jsonify(post.read())
            except Exception as e:
                # Return an error message in case of failure
                return jsonify({"error": str(e)}), 500

        def delete(self):
            try:
                # Obtain the request data
                data = request.get_json()
                # Find the BinaryConverter entry from the database
                post = BinaryConverter.query.get(data['id'])
                if not post:
                    return jsonify({"error": "Post not found"}), 404
                # Delete the post
                post.delete()
                # Return success message
                return jsonify({"message": "Post deleted"}), 200
            except Exception as e:
                # Return an error message in case of failure
                return jsonify({"error": str(e)}), 500

    # Add the resource to the API
    api.add_resource(_CRUD, '/binary-converter')

if __name__ == '__main__':
    app.run(debug=True)
