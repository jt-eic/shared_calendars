import os
from datetime import datetime, timedelta
# import datetime
# import pytz
###  Calendar Tools imported back  ***************************************
from datetime import datetime
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from calendar_tools import *


import sys, os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'onecalendar.settings'

# sys.path = sys.path + ['/onecalendar/']

django.setup()

from django.contrib.auth import get_user_model
from events.models import AllEvents
from account.models import CalendarProfile

'''
flow from this: go through each user calendar ID and get the events. 
Dump into the db, saving the initial cal_id from the owner who generated it.

'''

# use for now but put in from DB later:
# calendarId = "6p6ak3td65phucrouhjk65r6jo@group.calendar.google.com"   # from DB and make a 
# personal_ID = "jasun.t@gmail.com"

def event_to_db(ev):
    '''summary, description, start, end, location, id (owners original)'''
    # ev = shape_event(ev)
    ev_rcpt, evcreated = db_events.update_or_create(cal_id=ev['cal_id'], defaults=ev) #causes match
    return ev_rcpt, evcreated


if __name__ == "__main__":
    CLIENT_SECRET_FILE = "keys.json"

    SCOPES = "https://www.googleapis.com/auth/calendar"

    scopes = [SCOPES]

    service = build_service()
    
    User = get_user_model()
    
    db_events = AllEvents.objects.all()  
    
    # simple dict to see if cals have a new updated date
    db_event_updated_dates = {x.cal_id: x.updated for x in db_events}
    
    profiles = CalendarProfile.objects.all()

    combine_calId_dict = {}  # dictionary to hold owner ID and each their 
    
    all_inserted_events = []
    
    ev_count = 0
    inserted_count = 0
    updated_count = 0
    
    events_to_update = []  # just the ID for which will get updated to EVERY user if it lands here.
    events_to_insert = []  # HERE to insert them, by cal-id

    for user in profiles:
        # each shared calendar ID
        sharedids = []
        sharedids.append(user.shared_1)
        sharedids.append(user.shared_2)
        sharedids.append(user.shared_3)
        sharedids.append(user.shared_4)
        
        # make a list of the ids, to iterate through instead?
        combine_calId_dict[user.id] = user.combined_cal_id
        owner = user.id
        usr_model = User.objects.filter(id=owner)
        # iterate through the IDs and pull events, save to local DB.
        for id in sharedids:
            if id:
                calevents = grab_events(service, id)
            if calevents:
                # ev_count += len(calevents)
                # format them ready for db
                for event in calevents:
                    ev_count += 1
                    print(f"is there 'cal_id' field? {event.keys()}")
                    if event['id'] in db_event_updated_dates.keys():
                        print(f"event IS in db. Does updated date match?")
                        if event['updated'] == db_event_updated_dates[event['id']]:
                            print(f"date is the same. skip it. {event['summary']}")
                            continue
                        else:
                            print(f"event {event['summary']} is new. Add it.")
                            shaped = shape_event(event)
                            shaped['owner'] = usr_model[0]
                            db_rcpt, entered = event_to_db(shaped) 
                            all_inserted_events.append(db_rcpt)
                            events_to_update.append(event['cal_id'])
                            updated_count += 1
                    else:
                        print(f"event {event['summary']} is new. Add it.")
                        shaped = shape_event(event)
                        shaped['owner'] = usr_model[0]
                        db_rcpt, entered = event_to_db(shaped)  # use this rcpt to enter back cal_ids for other users insert
                        all_inserted_events.append(db_rcpt)
                        inserted_count += 1
                        events_to_insert.append(event['cal_id'])
                        print(f"to db? {entered}")
                # insert to db
                print(f" sum of all events so far: {ev_count}")
    
    # refresh db_Events and start working them into user shared cals
    db_events = AllEvents.objects.all()
    # loop db events, need to check either:
    # A: event_ID from user is on the event yet, and send 'patch' if it does.

    all_to_update = events_to_insert + events_to_update

    for item in db_events:
        # remove whos the owner from the combine_calID_dict so it doesn't send to them.
        # owner = combine_calId_dict.pop(item.owner.id) ## BAD IDEA. need this for later
        non_owners = {k: v for k, v in combine_calId_dict.items() if k != item.owner.id}
        print(f"these are the users who will get the pushed event: {non_owners.keys()}")
        try:
            event_ids = ast.literal_eval(item.other_ids)  # can this work??? Would be best if it becomes a dict.. then it can grow if we add people
        except SyntaxError:
            print('eventIds empty')
            event_ids = {}
        except ValueError:
            print(f'eventIds None? {item.other_ids}')
            event_ids = {}

        if event_ids:
            for k, evid in event_ids.items():
                if item.cal_id not in all_to_update:
                    print('does not need update.')
                    continue
                rcp = patch_event(service, non_owners[k], evid, item.__dict__)
                print(f'updates went successfully. {rcp["id"]}')
        else:
            # B: if not, do INSERT event if NOT the owner.
            event_ids = {} 
            for k, calid in non_owners.items():
                if item.cal_id not in all_to_update:
                    print('does not need insert.')
                    continue
                rcpt = insert_event(service, calid, item.__dict__)
                event_ids[k] = rcpt['id']
            item.other_ids = event_ids
            item.save()

        # C: delete (maybe in front) if event goes away?
    
    
    
    test_event = {'summary': 'test item',
                  'description': 'fill in desc.',
                  'start': {'dateTime': '2022-10-08T11:30:00-06:00', 'timeZone': 'America/Denver'},
                  'end': {'dateTime': '2022-10-08T12:30:00-06:00', 'timeZone': 'America/Denver'},
                  'updated': '2022-09-01T02:21:53.913Z',
    }
                  
    
    # 