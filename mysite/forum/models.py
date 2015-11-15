from django.db import models

# Create your models here.

from django.db import models

class Thread(models.Model):
    pub_date = models.DateTimeField('date published')
    username = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    # optional field
    description = models.CharField(max_length=200, null=True)

class Comment(models.Model):
    pub_date = models.DateTimeField('date published')
    username = models.CharField(max_length=50)
    text = models.CharField(max_length=300)
    score = models.IntegerField(default=0)
