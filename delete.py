from google_calendar import get_service, delete_event

with open('events.log', 'r') as f:
    eventIds = f.read().split('\n')

service = get_service()
for event in eventIds:
    delete_event(event, service)

