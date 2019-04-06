from django.contrib import admin
from account.models import Patient
from account.models import Profile
from account.models import Doctor
from account.models import Nurse

admin.site.register(Patient)
admin.site.register(Profile)
admin.site.register(Doctor)
admin.site.register(Nurse)
