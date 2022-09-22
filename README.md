# shared_calendars
small django project with Google calendar API, to sync multiple cals into one single calendar.

For family or group of friends, who each maintain one (or multiple) calendars then share them with others. Rather than sharing individually, 
each calendar is shared with a Google service account. 

Users also have a combined calendar they create in Google, then share that ID with the service account as well.

The events are stored to the DB with Django, as to have an easy admin area to look at items if there is any issues.

The DB also contains fields to handle shared users calendar IDs when it pushes back to their combined calendar. A single event will have
the owners calendar ID with the event data, plus the IDs of the new created event to pass to the other users.

If a new event is added, it gets combined with everything and works in the sync file.

If an updated event (determined by updated date mismatch) it will then push an update to that event for each user.

Now several calendars from MANY users all can be viewed by any individual who has a 'combined calendar' in one single calendar.

NOTE: The originator of an event will not get the events shared back to their combined calendars, as this would be totally silly
and redundant.  Could add an option within the django app to choose if it will sync back or not, but have not done that yet.

ALSO, item to add at some point would be to change the colorId of each users events, therefor separating out them by colors to
make viewing a little cleaner.

----   How to set it up: -------
# shared_calendars
small django project with Google calendar API, to sync multiple calendars into one single calendar.
Each user can provide multiple calendars they manage for sharing, and/ or only receive the events 
dumped into one combined calendar.

To share: you first need to get a google cloud account and enable the calendar API.  Then with the
credentials, you receive the .json key file to the API and include that in the sync_cals.py file.

Then this project is actualy a Django instance that needs to be created migrations and migrate.
Then add users, and each user profile has the fields needed to do the rest of the work.

For each user, they need to do 2 things: take the service account email address and share their
calendar(s) to that like its another user, and enable "make changes to events". This will not 
cause any actual changes from running this code, it does seem to be necessary in order to 
capture all of the event details. Only enabling the "see event details only" doesn't seem to work 
properly. Namely, it disables capturing the event ID which is critical for keeping track of all
this stuff.

Next, the shared ID from each calendar shared needs to be saved to the users profile in the Django app.

Combined calendar:
This one is where each user who is to receive what is shared, also created one for holding all of the
events they want to see.  This being the combined calendar; also needs the same settings applied as
above. The shared ID within the settings, goes to the combined ID field. Also need to share to the 
service account email and DEFINITELY needs to make changes to events; as this is the whole point.

Running the code: 
once all of the components are set up and entered, it works great by running as a cron job on a linux 
system. If running on a raspberry pi, I've not had much luck with the standard Pi raspian OSs unless 
you can get django to install correctly. Instead I installed a copy of ubuntu server on a Pi-4, and this
works great.

*****************
