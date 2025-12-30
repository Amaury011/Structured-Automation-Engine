from flask import request, Blueprint, jsonify
from models.webhook_event import WebhookEvent3, db
import hashlib, json

wh_bp = Blueprint("wh_bp", __name__)


@wh_bp.post("/test")
def webhook_test():
    data = request.json or {}

    phone = data.get("phone")
    if not phone:
        return {"error": "phone required"}, 400

    # idempotency check: prevent duplicate webhook events from creating multiple rows

    existing = WebhookEvent3.query.filter_by(phone=phone).first()
    if existing:
        return {"received": True, "duplicate": True}

    event = WebhookEvent3(
        name=data.get("name"),
        phone=phone,
        payload=data,
        status="received"
    )

    db.session.add(event)
    db.session.commit()

    return {"received": True}


@wh_bp.get("/events")
def list_events():
    events = WebhookEvent3.query.order_by(WebhookEvent3.created_at.desc()).all()
    return jsonify([
        {
            "id": e.id,
            "name": e.name,
            "phone": e.phone,
            "payload": e.payload,
            "status": e.status,
            "created_at": e.created_at.isoformat()
        }
        for e in events
    ])

@wh_bp.post("/process")
def process_events():
    from services.webhook_processor import process_pending
    process_pending()
    return {"status": "processing triggered"}

