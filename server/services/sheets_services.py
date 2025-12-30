import os, json, base64
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1rnt8EvfIEOywmRQGBlN6i4SYHeTIcWbS4Q5VYgDuh_0"

def get_sheets_client():
    raw = base64.b64decode(
        os.environ["GOOGLE_CREDENTIALS_JSON_B64"]
    ).decode("utf-8")

    creds_info = json.loads(raw)
    creds = Credentials.from_service_account_info(
        creds_info, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)
def read_test_cell():
    service = get_sheets_client()
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="A1"
    ).execute()
    return result.get("values", [])
def find_row_by_phone(phone):
    service = get_sheets_client()
    sheet = service.spreadsheets()

    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="A:E"
    ).execute()

    rows = result.get("values", [])

    for idx, row in enumerate(rows[1:], start=2):  # skip header
        if row and row[0] == phone:
            return idx, row

    return None, None

def upsert_contact(phone, name="", contact_id="", status="pending"):
    service = get_sheets_client()
    sheet = service.spreadsheets()

    row_num, _ = find_row_by_phone(phone)
    values = [[phone, name, contact_id, status, datetime.utcnow().isoformat()]]

    if row_num:
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"A{row_num}:E{row_num}",
            valueInputOption="RAW",
            body={"values": values}
        ).execute()
        return "updated"
    else:
        sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="A:A",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": values}
        ).execute()
        return "created"