from django.db import models
from django.conf import settings


class AllEvents(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    cal_id = models.CharField(max_length=150)
    start = models.CharField(max_length=60)
    end = models.CharField(max_length=60)
    summary =  models.CharField(max_length=100)
    description = models.TextField()
    location =  models.CharField(max_length=100)
    updated = models.CharField(max_length=50, null=True, blank=True)
    # need a cell to hold other users cal_id data? try as dict?
    other_ids = models.TextField(null=True, blank=True, help_text="not used here, unless json works. use single fields.")
    
    # share with all users besides the original owner
    usershare1 = models.CharField(max_length=250, null=True, blank=True)
    usershare2 = models.CharField(max_length=250, null=True, blank=True)
    usershare3 = models.CharField(max_length=250, null=True, blank=True)
    usershare4 = models.CharField(max_length=250, null=True, blank=True)
    
    class Meta:
        verbose_name = "Calendar Event"
        verbose_name_plural = "Calendar Events"


    def __str__(self):
            # userstr = str(self.owner)
            return self.summary

    