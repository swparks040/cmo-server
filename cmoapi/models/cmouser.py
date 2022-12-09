from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class CMOUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_position = models.TextField()
    salary = models.BigIntegerField()
    birthday = models.DateField()
    date_hired = models.DateField()
    date_evaluated = models.DateField()
    profile_image_url = models.TextField()
    
    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def username(self):
        return f'{self.user.username}'
