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
from tqdm import tqdm 

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

class Interact:
    
    def __init__(self,scopes):
        self.scopes = scopes
        self.get_service()
        self.eventIds = [] 
    
    def get_service(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle','rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json',self.scopes)
                creds = flow.run_local_server(port=0)
            with open('token.pickle','wb') as token:
                pickle.dump(creds,token)
        
        self.service = build('calendar','v3',credentials=creds)

    def list_events(self):
        now = datetime.utcnow().isoformat()+'Z'
        print('Gettting the upcoming 10 events')
        events_result = self.service.events().list(
                calendarId='primary',timeMin=now,
                maxResults=10,singleEvents=True,
                orderBy='startTime').execute()
        events = events_result.get('items',[])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime',event['start'].get('date'))
            print(start,event['summary'])

    def insert_events(self,df):
        today = datetime.today()
        start = today.weekday() % 6 + 1
        #filling up one date completely first
        for day in tqdm(range(start,7),desc='Progress'):
            for dtime in tqdm(range(1,9),desc=f'{today}'): 
                if df[day][dtime] == '':
                        if 'break' in df[1][dtime].lower():
                            summary = df[1][dtime]
                        else:
                            summary = df[day][dtime - 1]
                else:
                    summary = df[day][dtime]
                timing = df[0][dtime].split('to')
                if timing[0].strip() >= '08:00' and timing[0].strip() < '12:00':
                    period = 'am'
                else:
                    period = 'pm'
                start_time = next(datefinder.find_dates(str(datetime.date(today)) + f' {timing[0]} {period}'))
                if timing[1].strip() >= '08:00' and timing[1].strip() < '12:00':
                    period = 'am'
                else:
                    period = 'pm'
                end_time = next(datefinder.find_dates(str(datetime.date(today)) + f' {timing[1]} {period}'))
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
                event = self.service.events().insert(calendarId='primary',body=event).execute()
                self.eventIds.append(event.get('id'))
            today = today + timedelta(days=1)
        print('Timetable Successfully uploaded to your Google Calendar')

    def delete_events(self):
        for eventId in tqdm(self.eventIds):
            self.service.events().delete(calendarId='primary',eventId=eventId).execute()
        self.eventIds = []
        
    def __len__(self):
        return len(self.eventIds)
