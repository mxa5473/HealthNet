from django.forms import ModelForm
from account.models import User, Profile, Patient, Doctor, Nurse
from django import forms


class UserForm(ModelForm):
    """
    this is a user form used when updating user information
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']




class ProfileForm(ModelForm):
    """
    this is a profile form used when updating profile information
    """
    class Meta:
        model = Profile
        fields = ['streetAddress', 'town', 'zipCode', 'state', 'phoneNumber', 'hospital_assignment']



class PatientForm(ModelForm):
    """
    this is a patient form used when updating patient information
    """

    class Meta:
        model = Patient
        fields = ['height', 'weight', 'age', 'doctor', 'allergies','isAdmitted',"insurance_id", "hospital_preferred"]



class DoctorForm(ModelForm):
    """
    this is a doctor form used when updating doctor information
    """

    class Meta:
        model = Doctor
        fields = ['type']


class NurseForm(ModelForm):
    """
    this is a nurse form used when updating doctor information
    """

    class Meta:
        model = Nurse
        fields = ['type']

