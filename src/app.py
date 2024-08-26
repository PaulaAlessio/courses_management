from flask import Flask
from src import pages, courses, groups, database, events
import os
from dotenv import load_dotenv

load_dotenv()
ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = "./uploads"
MAX_CONTENT_PATH = 500000

app = Flask(__name__)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_PATH"] = MAX_CONTENT_PATH
app.register_blueprint(pages.bp)
app.register_blueprint(courses.bp)
app.register_blueprint(groups.bp)
app.register_blueprint(events.bp)
app.config.from_prefixed_env()
print(f"Current Environment: {os.getenv('ENVIRONMENT')}")
print(f"Using Database: {app.config.get('DATABASE')}")
print(f"Using PythonPath: {app.config.get('PYTHONPATH')}")

database.init_app(app)
if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=3000)
