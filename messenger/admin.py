from django.contrib import admin
from messenger.models import Message, Thread

admin.site.register(Message)
admin.site.register(Thread)
