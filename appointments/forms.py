from django.forms import ModelForm
from appointments.models import Appointment
from django import forms
import datetime
from account.models import Patient

class AppointmentForm(ModelForm):
    """
    this form is used to create a new appointment
    """

    class Meta:
        model = Appointment
        fields = ["doctor", "date", "time", "short_reason", "reason","hospital"]


    def clean_time(self):
        """
        this function checks if the doctor already has an appointment scheduled for
        the selected time
        """

        time = self.cleaned_data.get('time')
        doctor = self.cleaned_data.get('doctor')
        date = self.cleaned_data.get('date')

        time_qs = Appointment.objects.filter(time=time, doctor=doctor, date=date)

        if time_qs.exists():

            raise forms.ValidationError("The doctor is not free during this period")

        return time


    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date

    reason = forms.CharField(widget=forms.Textarea(
        attrs={'width': "100%", 'cols': "30", 'rows': "4", "height": "20%", "style": "resize:none;"}))


class AppointmentFormDoctor(ModelForm):
    """
    this form is used to create a new appointment for doctors
    """

    class Meta:
        model = Appointment
        fields = ["patient", "date", "time", "short_reason", "reason","hospital"]

    reason = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "30", 'rows': "4","height":"20%" ,"style":"resize:none;"}))



    def clean_time(self):
        """
        this function checks if the doctor already has an appointment scheduled for
        the selected time
        """

        time = self.cleaned_data.get('time')
        date = self.cleaned_data.get('date')

        time_qs = Appointment.objects.filter(time=time, date=date)

        if time_qs.exists():
            raise forms.ValidationError("The patient already has an appointment at this time")

        return time

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date


class AppointmentFormNurse(ModelForm):
    """
    this form is used to create a new appointment for nurses
    """

    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "date", "time", "short_reason", "reason","hospital"]

    def clean_time(self):
        """
        this function checks if the doctor already has an appointment scheduled for
        the selected time
        """

        time = self.cleaned_data.get('time')
        doctor = self.cleaned_data.get('doctor')
        date = self.cleaned_data.get('date')
        patient = self.cleaned_data.get('patient')

        time_qs_doc = Appointment.objects.filter(time=time, doctor=doctor, date=date)

        time_qs_pat = Appointment.objects.filter(time=time, patient=patient, date=date)


        if time_qs_doc.exists():

            raise forms.ValidationError("The doctor is not free during this period")

        if time_qs_pat.exists():

            raise forms.ValidationError("The patient already has an appointment at this time")

        return time

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date




    reason = forms.CharField(widget=forms.Textarea(
        attrs={'width': "100%", 'cols': "30", 'rows': "4", "height": "20%", "style": "resize:none;"}))



