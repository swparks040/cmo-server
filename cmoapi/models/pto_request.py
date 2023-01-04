from django.db import models
from datetime import date

class PTORequest(models.Model):

    cmouser = models.ForeignKey('CMOUser', on_delete=models.CASCADE)
    pto = models.ForeignKey('PTO', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    days_requested = models.IntegerField()
    justification = models.CharField(max_length=275)
    is_approved = models.BooleanField(default=False)