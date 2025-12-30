from models.webhook_event import WebhookEvent3, db
from services.sheets_services import upsert_contact
from services.contacts_service import get_people_client, upsert_people_contact

MAX_RETRIES = 3

def process_pending():
    people = get_people_client()

    events = (
    WebhookEvent3.query
    .filter(WebhookEvent3.status.in_(["received", "error"]))
    .filter(WebhookEvent3.status != "processing") # Concurrency protection
    .all()
)

    #De
    for event in events:
        # mark as processing so the next scheduler run (every 60s) does not re-process
        # this event while it is still being handled
        event.status = "processing"
    db.session.commit()

    for event in events:
        try:
            result = upsert_contact(
                phone=event.phone,
                name=event.name
            )
            contact_result = upsert_people_contact(
                service=people,
                name=event.name,
                phone=event.phone
            )

            event.status = f"sheet_{result}_contact_{contact_result}"

        except Exception:
            event.status = "error"

    db.session.commit()
