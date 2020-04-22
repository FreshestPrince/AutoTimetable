from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, tools
import google_auth_oauthlib.flow
from datetime import datetime


# If modifying these scopes, delete the file token.pickle.
SCOPES = "https://www.googleapis.com/auth/calendar"
store = file.Storage('token.json')
creds = store.get()

if not creds or creds.invalid:
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret_864541978291-0as7r6qqem433u8ivrr22eioltfio4us.apps.googleusercontent.com.json",
        ['https://www.googleapis.com/auth/drive.metadata.readonly'])
    flow.redirect_uri = 'https://www.google.com/oauth2callback'
    #flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
    # This next section's code will be here
    if calendar_list_entry['accessRole']:
        startTime = datetime.strptime(
            input("Please enter in the start time for the event in this format: (ex. September 02, 2018, 09:00PM) "),
            '%B %m, %Y, %I:%M%p').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        endTime = datetime.strptime(
            input("Please enter in the end time for the event in this format: (es. September 03, 2018, 11:25AM) "),
            '%B %m, %Y, %I:%M%p').strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        event = {
            'summary': input("What's the name of the event? "),
            # You can put inputs like this in dictionaries - it's stored in the key value directly, so there's no reason why not to. Continue to do this for all the information
            # you need in the event, except for the times, which are already done
            'location': "a",
            'description': "a",
            'start': {
                'dateTime': startTime,
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': endTime,
                'timeZone': 'America/New_York',
            },
        }
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))