from django.db import models
from datetime import date

class Message(models.Model):

    cmouser = models.ForeignKey('CMOUser', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateField(default=date.today)
    content = models.TextField()
