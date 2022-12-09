from django.db import models

class PTO(models.Model):

    cmouser = models.ForeignKey('CMOUser', on_delete=models.CASCADE)
    total_days = models.IntegerField()
    days_used = models.IntegerField()
    days_remaining = models.IntegerField()
