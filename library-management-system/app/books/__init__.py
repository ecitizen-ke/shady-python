from flask import Blueprint, request, jsonify
import os

book_bp = Blueprint("book_bp", __name__)

books = []


@book_bp.route("/books")
def fetch_books():
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
    return books


@book_bp.route("/books/create", methods=["POST"])
def create_book():
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

    book = {"id": len(books) + 1, "title": "", "description": ""}
    book["description"] = request.get_json().get("description")
    book["title"] = request.get_json().get("title")
    books.append(book)
    return book


@book_bp.route("/book/update/<int:id>", methods=["POST"])
def update_book(id):
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

    if len(books) == 0:
        return jsonify({"message": "Book Not Found"})

    book = next((book for book in books if book["id"] == id), None)
    if not book:
        return jsonify({"message": "Book Not Found"}), 400

    if not request.get_json():
        return jsonify({"message": "No data provided"}), 400
    book["description"] = request.get_json().get("description")
    book["title"] = request.get_json().get("title")

    return jsonify(book), 200


@book_bp.route("/books/delete/<int:id>", methods=["DELETE"])
def delete_book(id):
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
    global books
    filtered_books = [book for book in books if book["id"] != id]

    if len(filtered_books) == len(books):
        return jsonify({"message": "Book Not Found"}), 404

    books = filtered_books
    return jsonify({"message": "Book Deleted Successfully"}), 200
