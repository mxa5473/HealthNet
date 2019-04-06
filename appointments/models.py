from __future__ import unicode_literals

from django.db import models
import datetime
from django import forms



class Appointment(models.Model):
    """
    this class represents an appointment in the system.
    An appointment is assigned to a patient, a doctor,
    and a location.

    Patients and Doctors are able to see appointments which belong
    to them. Nurses are able to see all appointments in their
    hospital
    """
    patient = models.ForeignKey("account.Patient", null=True, blank=True)
    doctor = models.ForeignKey("account.Doctor", null=True, blank=True)

    hospital = models.ForeignKey("administration.Hospital",null=True,blank=True)

    date = models.DateField(default=datetime.date.today)


    TIME_CHOICES = (
        ('01','1:00 AM'), ('02','2:00 AM'), ('03','3:00 AM'), ('04','4:00 AM'), ('05','5:00 AM'), ('06','6:00 AM'),
        ('07', '7:00 AM'), ('08', '8:00 AM'), ('09','9:00 AM'), ('10','10:00 AM'), ('11','11:00 AM'),
        ('12', '12:00 PM'), ('13', '1:00 PM'), ('14', '2:00 PM'), ('15','3:00 PM'), ('16','4:00 PM'), ('17','5:00 PM'),
        ('18', '6:00 PM'), ('19', '7:00 PM'), ('20', '8:00 PM'),('21','9:00 PM'), ('22','10:00 PM'), ('23','11:00 PM'),
        ('00', '12:00 AM')

    )

    time = models.CharField(max_length=2, choices=TIME_CHOICES)

    short_reason = models.CharField(max_length=15)
    reason = models.TextField(max_length=500)

    def datetimeToString(self):
        return self.date.isoformat()+"T"+self.time[0:4]

    def __str__(self):
        # to string function
        return self.patient.profile.user.last_name +" "+self.short_reason
