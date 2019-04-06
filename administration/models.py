from __future__ import unicode_literals

from django.utils import timezone

from django.db import models
import datetime


class Log(models.Model):
    """
    A log consists of several fields which describe an action taken within the app.
    """

    # the username of the user who completed the action
    username = models.CharField(max_length=30)

    # the action (verb)
    action = models.CharField(max_length=30)

    # the time of the action
    time = models.DateTimeField(default=timezone.now)





class Stat(models.Model):

    name = models.CharField(max_length=30)
    value = models.IntegerField(default=0)

    # to string function
    def __str__(self):
        return self.name





class Hospital(models.Model):
    """
    A hospital consists of several fields which describe a hospital
    """

    # the name of this hospital
    name = models.CharField(max_length=30)

    # address of this hospital
    address = models.CharField(max_length=30)

    # to string function
    def __str__(self):
        return self.name



