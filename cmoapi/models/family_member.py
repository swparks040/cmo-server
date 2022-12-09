from django.db import models
from datetime import date

class FamilyMember(models.Model):

    cmouser = models.ForeignKey('CMOUser', on_delete=models.CASCADE)
    family_member_relationship = models.ForeignKey('FamilyMemberRelationship', on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField()
    birthday = models.DateField()
    anniversary = models.DateField()
    graduation = models.DateField()