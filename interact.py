from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime,timedelta
import os
import pickle
import json 
import sys
import datefinder
from utils import extract_df

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

#better option would be to create a class
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
    eventIds = []
    today = datetime.today()
    start = today.weekday() % 6 + 1
    df = extract_df('timetable.pdf')    
    #filling up one date completely first
    for day in range(start,7):
        for dtime in range(1,9): 
            if df[day][dtime] == '':
                    if 'break' in df[1][dtime].lower():
                        summary = df[1][dtime]
                    else:
                        summary = df[day][dtime - 1]
            else:
                summary = df[day][dtime]
            timing = df[0][dtime].split('to')
            start_time = next(datefinder.find_dates(str(datetime.date(today)) + f' {timing[0]} pm'))
            end_time = next(datefinder.find_dates(str(datetime.date(today)) + f' {timing[1]} pm'))
            timezone = 'Asia/Kolkata'
            event = {
                'summary':summary,
                'location':'PICT,Pune',
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
            eventIds.append(event.get('id'))
        print(f'{datetime.date(today)} done ')
        today = today + timedelta(days=1)
    print('Timetable Successfully uploaded to your Google Calendar')
    return eventIds

def delete_events(service,eventIds):
    if isinstance(eventIds,str):
        eventIds = [eventsIds]
    for eventId in eventIds:
        service.events().delete(calendarId='primary',eventId=eventId).execute()


