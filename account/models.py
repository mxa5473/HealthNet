from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from administration.models import Hospital
from django import forms


class Profile(models.Model):
    """
    A profile is an extension of Django's user model. It adds fields
    which pertain to all types of HealthNet's users. A profile should
    not be created on its own, as it is created when a new patient, nurse
    or doctor is registered.
    """

    # the user is the user which is tied to this profile
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # add additional fields here
    streetAddress = models.CharField(max_length=30, blank=True, null=True)
    town = models.CharField(max_length=30, blank=True, null=True)
    zipCode = models.CharField(max_length=5, null=True, blank=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    phoneNumber = models.CharField(max_length=13, null=True, blank=True)

    # the hospital this user is assigned to
    hospital_assignment = models.ForeignKey(Hospital, null=True, blank=True)

    # to string function
    def __str__(self):
        return self.user.last_name + ", " + self.user.first_name


class Doctor(models.Model):
    """
    A doctor is associated with patients in HealthNet. When a doctor is
    registered, a new User, profile, and doctor are created. These are
    associated with eachother until the doctor is deleted.
    """

    # this is the doctor's profile
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    # doctor fields
    type = models.CharField(max_length=30, blank=True, null=True)


    # returns a list of patients which belong to this doctor
    def get_patients(self):
        Patient.objects.filter(doctor=self)

    # the doctors to string method
    def __str__(self):
        return "Dr. " + self.profile.user.last_name

    def getUserType(self):
        return "Doctor"


class Patient(models.Model):
    """
    A patient is the general user of our system. This is the
    only type of user which can self-register outside of the admin
    console. Patients required some basic fields which can be edited
    later on.
    """

    # this is the patient's profile
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # an optional field which specifies who the patients doctor is
    doctor = models.ForeignKey(Doctor, blank=True, null=True)

    # preferred hospital
    hospital_preferred = models.ForeignKey(Hospital, null=True, blank=True)


    # an optional field which are notes on the patient. Only a doctor
    # or nurse can edit these notes
    #notes = models.TextField(max_length=100, blank=True)

    # insurance identification number
    insurance_id = models.CharField(max_length=10, blank=True, null=True)

    # patient information fields
    height = models.CharField(max_length=5, blank=True, null=True)
    weight = models.CharField(max_length=5, blank=True, null=True)
    age = models.CharField(max_length=3, null=True, blank=True)
    allergies = models.CharField(max_length=50, null=True, blank=True)

    CHOICES = (("YES","YES"),("NO","NO"))

    isAdmitted = models.CharField(max_length=3, null=True, blank=True, choices=CHOICES)



    # this is a patients to string function
    def __str__(self):
        return self.profile.user.last_name + ", " + self.profile.user.first_name

    def getUserType(self):
        return "Patient"

    def getFullName(self):
        return self.profile.user.last_name + ", " + self.profile.user.first_name



class Nurse(models.Model):
    """
    A nurse is associated with patients in HealthNet. When a nurse is
    registered, a new User, profile, and nurse are created. These are
    associated with each other until the nurse is deleted.
    """

    # this is the nurse's profile
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    # nurse fields
    type = models.CharField(max_length=30, blank=True)

    # returns a list of all patients
    def get_patients(self):
        return Patient.objects.all()

    # the nurse to string method
    def __str__(self):
        return self.profile.user.first_name + " " + self.profile.user.last_name

    def getUserType(self):
        return "Nurse"

