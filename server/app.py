from flask import Flask
from flask_cors import CORS
from blueprints.webhook_route import wh_bp
from models.webhook_event import db
from services.scheduler import start_scheduler
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

database_url = os.getenv("DATABASE_URL")

if database_url and "sslmode=" not in database_url:
    database_url += "?sslmode=require"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

start_scheduler(app)

app.register_blueprint(wh_bp, url_prefix="/api/webhook")

@app.route("/")
def root():
    return {"status": "ok", "service": "structured-automation-engine"}

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run()
