from datetime import datetime
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import ast

svc_acc_email = "catchall-cals@homecals.iam.gserviceaccount.com"

CLIENT_SECRET_FILE = "keys.json"

SCOPES = "https://www.googleapis.com/auth/calendar"

scopes = [SCOPES]


def build_service():
    ''' use repurposed service function from MTVG calendar tools.
    Modified to get personal calendar data'''

    CLIENT_SECRET_FILE = "keys.json"

    SCOPES = "https://www.googleapis.com/auth/calendar"

    scopes = [SCOPES]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        filename=CLIENT_SECRET_FILE,
        scopes=SCOPES)

    http = credentials.authorize(httplib2.Http())

    service = build('calendar', 'v3', http=http)

    return service


def grab_events(service, cal_id):
    wnow = datetime.utcnow().isoformat() + 'Z'
    now = datetime.today().isoformat() + "T00:00:00.000000Z"
    print(f"WTF is the date it caught???, {now}, \nold version: , {wnow}")
    '''gathering existing events to compare modified dates'''
    allevents = service.events().list(calendarId=cal_id,
                                        timeMin=wnow,
                                        maxResults=200, singleEvents=True,
                                        orderBy='startTime').execute()
    events = allevents.get('items', [])
    return events



def shape_event(ev):
    '''drops and renames some fields to make it work for the db'''
    drop_fields = ['htmlLink', 'kind', 'etag', 'status', 'creator', 'organizer', 'transparency', 
                   'iCalUID', 'sequence', 'reminders', 'eventType', 'created', 'visibility', 'colorId',
                   'conferenceData', 'hangoutLink', 'attendees', 'originalStartTime', 'recurringEventId',
                   'extendedProperties',]
    
    keepers = ('summary', 'description', 'location', 'start', 'end', 'updated',)
    
    # has to happen for matching event to calendar
    if 'id' in ev:
        ev['cal_id'] = ev.pop('id')

    for f in drop_fields:
        try:
            ev.pop(f)
        except KeyError:
            print(f"field << {f} >> doesn't exist")
            continue

    for k in keepers:
        if k not in ev.keys():
            ev[k] = 'empty'
    return ev


def make_payload(ev):
    pass


def insert_event(service, cal_id, payload):
    ''' service from service account credentials,
    goog_user_id is just their google email address( default if no cal_id)
    cal_id is only the user email OR custom calendar ID if  they don't have some other cal name.
    payload is the item to have inserted in the calendar.
    '''
    
    keepers = ('summary', 'description', 'location', 'start', 'end',)

    newone = {k: payload[k] for k in payload if k in keepers}
    newone['start'] = ast.literal_eval(newone['start'])
    newone['end'] = ast.literal_eval(newone['end'])
    
    if newone['start'] == newone['end']:
        print(f" start and end are the same. Fix this so it doesn't cancel itself? {newone['start']}")
    # print(f"the event?\n{newone}")

    print(f"the event before inserting:  {newone['summary']} -->>>   \n")
    event = service.events().insert(calendarId=cal_id, body=newone).execute()

    return event


def patch_event(service, cal_id: str, event_id: str, payload: dict):
    '''
    same as sends, but takes EVID and patches existing instead of making new...
    need to id IF 
    '''
    # hand off as other variable
        
    keepers = ('summary', 'description', 'location', 'start', 'end',)

    newone = {k: payload[k] for k in payload if k in keepers}
    newone['start'] = ast.literal_eval(newone['start'])
    newone['end'] = ast.literal_eval(newone['end'])

    event = service.events().patch(calendarId=cal_id, eventId=event_id, body=newone).execute()

    return event


def delete_event(service, cal_id, event_id):
    ''' from within a sync operation; this should delete an event sending FROM this system
    should it be removed; pulled from the server; then no match to sync back to then DELETE'''

    rec = service.events().delete(calendarId=cal_id, eventId=event_id).execute()
    print('delete successful. return receipt if any: ', rec)
    return rec