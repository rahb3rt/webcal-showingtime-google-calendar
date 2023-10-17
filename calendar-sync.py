import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
from icalendar import Calendar, Event

SCOPES = ['https://www.googleapis.com/auth/calendar']
email = os.getenv('EMAIL')
url = f'https://www.googleapis.com/calendar/v3/calendars/{email}/events'
calendar = "https://showingti.me/cal/GpFp7GIp9SYB9sc8"

response = requests.get(calendar)
with open('output.ics', 'wb') as f:
    f.write(response.content)


# Load credentials.json and authenticate
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=8080)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

# Convert ICS to JSON (using icalendar and some parsing)
with open('output.ics', 'rb') as f:
    cal = Calendar.from_ical(f.read())
    events_to_add = []
    for component in cal.walk():
        if isinstance(component, Event):
            events_to_add.append({
                'summary': str(component.get('summary')),
                'description': str(component.get('description')),
                'location': str(component.get('location')),
                'start': {'dateTime': component.get('dtstart').dt.isoformat(), 'timeZone': 'America/New_York'},
                'end': {'dateTime': component.get('dtend').dt.isoformat(), 'timeZone': 'America/New_York'},
            })


# Fetch events from Google Calendar
response = requests.get(
    url,
    headers={'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'},
    params={'timeMin': events_to_add[0]['start']['dateTime'], 'timeMax': events_to_add[-1]['end']['dateTime']}
)
existing_events = response.json().get('items', [])

# Check for duplicates and add unique events
for event in events_to_add:
    if not any(
            e['start']['dateTime'] == event['start']['dateTime'] and
            e['end']['dateTime'] == event['end']['dateTime'] and
            e['summary'] == event['summary'] for e in existing_events):
        response = requests.post(
            url,
            headers={'Authorization': f'Bearer {creds.token}', 'Content-Type': 'application/json'},
            json=event
        )
        print(response.text)

