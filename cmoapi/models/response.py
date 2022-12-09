from django.db import models
from datetime import date

class Response(models.Model):

    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    author = models.ForeignKey('CMOUser', on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateField(default=date.today)

