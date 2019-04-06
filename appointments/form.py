from django.forms import ModelForm
from appointments.models import Appointment
from django import forms


class AppointmentForm(ModelForm):
    """
    this form is used to create a new appointment
    """

    class Meta:
        model = Appointment
        fields = ["doctor", "date", "time", "short_reason", "reason"]


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


class AppointmentFormDoctor(ModelForm):
    """
    this form is used to create a new appointment for doctors
    """

    class Meta:
        model = Appointment
        fields = ["patient", "date", "time", "short_reason", "reason"]



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


class AppointmentFormNurse(ModelForm):
    """
    this form is used to create a new appointment for nurses
    """

    class Meta:
        model = Appointment
        fields = ["patient", "doctor", "date", "time", "short_reason", "reason"]

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
