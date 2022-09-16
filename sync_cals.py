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

    ''' *********************************************************************************************************
    ##    Start loop for user data, gathering their source calendars and searching for new or updates  **********
    Summary:
    from the user profile, iterates through shared calendar IDs in order to pull from their source calendar(s).
    by grab_events function(service, and calendarID)
    Also prepares DB copy by making a simple dictionary with cal_ids to easily verify if the event exists yet.

    comparing event IDs against the dictionary, it can tell if:
    there IS a matching id, check the updated date. IF dates DON'T match, then do updates.
    there IS NOT a match, then this one is new and needs to be inserted.

    for items checked from DB, and there is not a matching calendar ID that was pulled from the original shared calendar,
    then it is candidate for delete.
    '''

    combine_calId_dict = {}  # dictionary to hold owner ID and each of their combined calendar; for managing their shared cal.

    all_inserted_events = []
    
    ev_count = 0
    inserted_count = 0
    updated_count = 0
    
    events_to_update = []  # just the ID for which will get updated to EVERY user if it lands here.
    events_to_insert = []  # HERE to insert them, by cal-id

    check_back_cal_ids = []  # for cleaning up; pile all of them up and see whats NOT a match in the db; if in DB but not here, delete it.

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
                    check_back_cal_ids.append(event['id'])   #  ADDED Immediately!

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
                calevents = []  # resets the list, so it doesn't re-run against itself if next ID is empty

    #  Now double-check for anything to delete...
    for delete_me in db_events:
        if delete_me.cal_id not in check_back_cal_ids:
            print(f"THIS ONE candidate for delete.. {delete_me.summary} date: {delete_me.start}")
            # do delete here..
    # holdup = input('waiting here...')

    ''' *************************************************************************************************************
    This section summary: 
    after the previous step of checking source data and bringing the database up to date, now run through it again
    and see what users need changes to their COMBINED calendars.

    * first pulls the DB again to operate on all new data.
    '''

    # refresh db_Events and start working them into user shared cals
    db_events = AllEvents.objects.all()
    # loop db events, need to check either:
    # A: event_ID from user is on the event yet, and send 'patch' if it does.

    all_to_update = events_to_insert + events_to_update  # combined list of IDs found to be either inserted or updated. ALL users source IDs

    for item in db_events:
        # remove whos the owner from the combine_calID_dict so it doesn't send to them.
        # owner = combine_calId_dict.pop(item.owner.id) ## BAD IDEA. need this for later
        non_owners = {k: v for k, v in combine_calId_dict.items() if k != item.owner.id}
        print(f"these are the users who will get the pushed event: {non_owners.keys()}")
        try:
            combined_ev_ids = ast.literal_eval(item.other_ids)  # THIS WORKS!! Yay
        except SyntaxError:
            print(f'eventIds empty {item.other_ids}')
            combined_ev_ids = {}
        except ValueError:
            print(f'eventIds None? {item.other_ids}')
            combined_ev_ids = {}

        # checking this event, IF its been pushed already then compare to all_to_update list:
        if combined_ev_ids:
            for k, evid in combined_ev_ids.items():
                if item.cal_id not in all_to_update:
                    print('does not need update.')
                    continue
                rcp = patch_event(service, non_owners[k], evid, item.__dict__)
                print(f'updates went successfully. {rcp["id"]}')
        else:
            # B: if not, do INSERT event if NOT the owner.
            combined_ev_ids = {} 
            for k, calid in non_owners.items():
                if item.cal_id not in all_to_update:
                    print('does not need insert.')
                    continue
                rcpt = insert_event(service, calid, item.__dict__)
                combined_ev_ids[k] = rcpt['id']
            item.other_ids = combined_ev_ids
            item.save()

