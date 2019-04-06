from django.db import models
from account.models import Doctor, Patient

class Prescription(models.Model):

    patient = models.ForeignKey("account.Patient")
    name = models.CharField(max_length=20, blank=True)
    dosage = models.CharField(max_length=20, blank=True)
    refills = models.PositiveIntegerField()
    doc = models.ForeignKey("account.Doctor")

    def __str__(self):
        return self.name + " " + self.dosage


class Test(models.Model):

    patient = models.ForeignKey("account.Patient")
    name = models.CharField(max_length=20, blank=True)
    comments = models.TextField(max_length=280, blank=True)
    # Note that a file will have to be allowed here, but not for R2B
    doc = models.ForeignKey("account.Doctor", null=True, blank=True)
    released = models.BooleanField(default=False)

    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name

class MedicalNote(models.Model):

    patient = models.ForeignKey("account.Patient", blank=True, null=True)
    doctor = models.ForeignKey("account.Doctor", blank=True, null=True)
    note = models.TextField(max_length=100, blank=True)


