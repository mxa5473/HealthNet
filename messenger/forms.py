from django.forms import ModelForm
from messenger.models import Thread, Message
from django import forms

class ThreadForm(ModelForm):
    """
    this is the form used to create a new thread
    """
    class Meta:
        model = Thread
        fields = ['user2', 'subject']

class MessageForm(ModelForm):
    """
    this is the form used to create a new message
    """
    class Meta:
        model = Message
        fields = ['text']

    text = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'rows': "4","height":"20%" ,"style":"resize:none;"}))