from django.db import models
import datetime
from django.utils import timezone

class Message(models.Model):

    """
    the message class represents a single message within a thread. A message has an
    @author - the sender of the message
    @datetime - the date and time the message was created
    @text - the text content of the message
    @thread - the thread this message belongs to
    """

    author = models.ForeignKey("account.Profile")
    text = models.TextField(max_length=500)
    datetime = models.DateTimeField(default=timezone.now)
    thread = models.ForeignKey("messenger.Thread", default=None)


class Thread(models.Model):

    """
    a thread consists of one or more messages share between two users. A thread has an
    @user1 - one of two users the thread is shared between - default is the user who creates the thread
    @user2 - one of the two users the thread is shared between
    """

    user1 = models.ForeignKey("account.Profile", related_name="user1")
    user2 = models.ForeignKey("account.Profile", related_name="user2")
    subject = models.CharField(max_length=20)

    def __str__(self):
        # to string function
        return str(self.id)
