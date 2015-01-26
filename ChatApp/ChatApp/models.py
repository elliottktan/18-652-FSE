from django.db import models

from django.contrib.auth.models import User

class Post(models.Model):
    text = models.CharField(max_length=300)
    user = models.ForeignKey(User)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.text
