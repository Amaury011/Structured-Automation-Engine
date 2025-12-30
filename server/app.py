from flask import Flask, Blueprint
from flask_cors import CORS
from blueprints.webhook_route import wh_bp
from flask_sqlalchemy import SQLAlchemy
from models.webhook_event import db
from services.scheduler import start_scheduler
import os
from dotenv import load_dotenv
load_dotenv()




app = Flask(__name__)
CORS(app, resources={r"/api/*"})

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db.init_app(app)

with app.app_context():
    db.create_all()

start_scheduler(app)

app.register_blueprint(wh_bp, url_prefix="/api/webhook")

@app.route('/')
def hello_world():
    return '<h1>Minimum Viable Product is live!</h1>'
@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True)