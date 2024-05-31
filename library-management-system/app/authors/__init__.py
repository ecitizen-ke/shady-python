from flask import Blueprint, request, jsonify
import os

author_bp = Blueprint("author_bp", __name__)

authors = []


@author_bp.route("/authors")
def fetch_authors():
    api_key = request.headers.get("x-api-key")
    if not api_key:
        return jsonify({"message": "API Key Not Present"}), 400

    # check if api key present in the env is the same as the api key in the request headers
    env_api_key = ""
    env = os.environ.get("ENV")
    if env == "development":
        env_api_key = os.environ.get("API_KEY_DEV")
    elif env == "production":
        env_api_key = os.environ.get("API_KEY_PROD")
    if api_key != env_api_key:
        return jsonify({"message": "Unauthorized"}), 401

    return authors


@author_bp.route("/authors/create", methods=["POST"])
def create_author():
    api_key = request.headers.get("x-api-key")
    if not api_key:
        return jsonify({"message": "API Key Not Present"}), 400

    # check if api key present in the env is the same as the api key in the request headers
    env_api_key = ""
    env = os.environ.get("ENV")
    if env == "development":
        env_api_key = os.environ.get("API_KEY_DEV")
    elif env == "production":
        env_api_key = os.environ.get("API_KEY_PROD")
    if api_key != env_api_key:
        return jsonify({"message": "Unauthorized"}), 401

    author = {"id": len(authors) + 1, "name": "", "book_id": "", "description": ""}
    author["name"] = request.get_json().get("name")
    author["description"] = request.get_json().get("description")
    author["book_id"] = request.get_json().get("book_id")
    authors.append(author)
    return author


@author_bp.route("/author/update/<int:id>", methods=["POST"])
def update_author(id):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        return jsonify({"message": "API Key Not Present"}), 400

    # check if api key present in the env is the same as the api key in the request headers
    env_api_key = ""
    env = os.environ.get("ENV")
    if env == "development":
        env_api_key = os.environ.get("API_KEY_DEV")
    elif env == "production":
        env_api_key = os.environ.get("API_KEY_PROD")
    if api_key != env_api_key:
        return jsonify({"message": "Unauthorized"}), 401

    if len(authors) == 0:
        return jsonify({"message": "Author Not Found"})

    author = next((author for author in authors if author["id"] == id), None)
    if not author:
        return jsonify({"message": "Author Not Found"}), 400

    if not request.get_json():
        return jsonify({"message": "No data provided"}), 400
    author["name"] = request.get_json().get("name")
    author["description"] = request.get_json().get("description")
    author["book_id"] = request.get_json().get("book_id")

    return jsonify(author), 200


@author_bp.route("/authors/delete/<int:id>", methods=["DELETE"])
def delete_author(id):
    api_key = request.headers.get("x-api-key")
    if not api_key:
        return jsonify({"message": "API Key Not Present"}), 400

    # check if api key present in the env is the same as the api key in the request headers
    env_api_key = ""
    env = os.environ.get("ENV")  # read current app env
    if env == "development":
        env_api_key = os.environ.get("API_KEY_DEV")
    elif env == "production":
        env_api_key = os.environ.get("API_KEY_PROD")
    if api_key != env_api_key:
        return jsonify({"message": "Unauthorized"}), 401
    global authors
    filtered_authors = [author for author in authors if author["id"] != id]

    if len(filtered_authors) == len(authors):
        return jsonify({"message": "Author Not Found"}), 404

    authors = filtered_authors
    return jsonify({"message": "Author Deleted Successfully"}), 200
