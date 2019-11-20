from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime,timedelta
import os
import pickle
import json 
import sys
import datefinder

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle','wb') as token:
            pickle.dump(creds,token)
    
    service = build('calendar','v3',credentials=creds)
    return service

def list_events(service):
    now = datetime.utcnow().isoformat()+'Z'
    print('Gettting the upcoming 10 events')
    events_result = service.events().list(
            calendarId='primary',timeMin=now,
            maxResults=10,singleEvents=True,
            orderBy='startTime').execute()
    events = events_result.get('items',[])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime',event['start'].get('date'))
        print(start,event['summary'])

def insert_events(service):
    with open('foo.json') as f:
        data = json.load(f)
    today = datetime.today()
    start = today.weekday() % 6 +1 
    #filling up one date completely first
    for day in range(start,7):
        for dtime in range(1,8): 
            summary = data[dtime][str(day)]
            tis = data[dtime]['0'].split()[0]
            tie = data[dtime]['0'].split()[2]
            start_time = next(datefinder.find_dates(str(datetime.date(today)) + f' {tis} pm'))
            end_time = next(datefinder.find_dates(str(datetime.date(today)) + f' {tie} pm'))
            timezone = 'Asia/Kolkata'
            event = {
                'summary':summary,
                'location':'PICT,Pune',
                'description':'Checking the working of the project',
                'start':{
                    'dateTime': start_time.isoformat(), 
                    'timeZone': timezone
                },
                'end':{
                    'dateTime':end_time.isoformat(),
                    'timeZone':timezone
                }
            }
            event = service.events().insert(calendarId='primary',body=event).execute()
        print(f'{datetime.date(today)} done ')
        today = today + timedelta(days=1)
    print('Timetable Successfully uploaded to your Google Calendar')
