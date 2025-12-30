from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WebhookEvent3(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # normalized fields
    name = db.Column(db.String(120))
    phone = db.Column(db.String(50))

    # raw payload (always keep)
    payload = db.Column(db.JSON, nullable=False)

    # processing state
    status = db.Column(db.String(20), default="received")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

