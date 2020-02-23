from django.db import models

# Create your models here.

class globalStatus(models.Model):
    country = models.CharField(max_length=50, blank=False)
    diagnosed = models.IntegerField()
    new_cases = models.IntegerField()
    death = models.IntegerField()
    new_death = models.IntegerField()
    discharged = models.IntegerField()
    critical = models.IntegerField()
    region = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)

class globalLastUpdate(models.Model):
    last_update = models.CharField(max_length= 100)