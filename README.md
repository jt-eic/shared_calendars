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

