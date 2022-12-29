from django.db import models
from datetime import date

class FamilyMember(models.Model):

    cmouser = models.ForeignKey('CMOUser', on_delete=models.CASCADE)
    family_member_relationship = models.ForeignKey('FamilyMemberRelationship', on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField()
    birthday = models.CharField(max_length=50)
    anniversary = models.CharField(max_length=50)
    graduation = models.CharField(max_length=50)
