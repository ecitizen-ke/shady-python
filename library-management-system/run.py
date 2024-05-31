from app import create_app
from app.books import book_bp
from dotenv import load_dotenv
from instance.config.setting import config

load_dotenv()


myapp = create_app(config)

myapp.register_blueprint(book_bp)

if __name__ == "__main__":
    myapp.run(debug=True)
