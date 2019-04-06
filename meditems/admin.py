from django.contrib import admin
from meditems.models import Test, Prescription, MedicalNote
# Register your models here.

admin.site.register(Test)
admin.site.register(Prescription)
admin.site.register(MedicalNote)