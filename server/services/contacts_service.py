import os, json, base64
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/contacts"]

def get_people_client():
    raw = base64.b64decode(
        os.environ["GOOGLE_CREDENTIALS_JSON_B64"] # add credentials 
    ).decode("utf-8")

    creds_info = json.loads(raw)
    creds = Credentials.from_service_account_info(
        creds_info,
        scopes=SCOPES
    )

    return build("people", "v1", credentials=creds)


def create_contact(name, phone):
    service = get_people_client()

    body = {
        "names": [{"givenName": name}] if name else [],
        "phoneNumbers": [{"value": phone}]
    }

    person = service.people().createContact(body=body).execute()
    return person["resourceName"]


def upsert_people_contact(service, name, phone):
    results = service.people().searchContacts(
        query=phone,
        readMask="names,phoneNumbers"
    ).execute()

    connections = results.get("results", [])

    if connections:
        person = connections[0]["person"]
        resource_name = person["resourceName"]

        service.people().updateContact(
            resourceName=resource_name,
            updatePersonFields="names",
            body={
                "names": [{
                    "givenName": name
                }]
            }
        ).execute()

        return "updated"
    else:
        service.people().createContact(
            body={
                "names": [{"givenName": name}],
                "phoneNumbers": [{"value": phone}]
            }
        ).execute()

        return "created"
