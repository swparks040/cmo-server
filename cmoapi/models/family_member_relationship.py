from django.db import models

class FamilyMemberRelationship(models.Model):

    label = models.CharField(max_length=50)