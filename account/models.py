from django.db import models
from django.conf import settings

# Create your models here.

class CalendarProfile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    combined_cal_id = models.CharField(max_length=500, null=True, blank=True)
    shared_1 = models.CharField(max_length=200, null=True, blank=True)
    shared_2 = models.CharField(max_length=200, null=True, blank=True)
    shared_3 = models.CharField(max_length=200, null=True, blank=True)
    shared_4 = models.CharField(max_length=200, null=True, blank=True)

    shared_calendars = models.TextField(null=True, blank=True, help_text="sandbox version, test this for json data.")

    class Meta:
        verbose_name = "Users Calendar Settings"
        
    def __str__(self):
        ownerstr = str(self.owner)
        return ownerstr
        