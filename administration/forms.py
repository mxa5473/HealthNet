from django.forms import ModelForm
from account.models import User, Profile, Patient, Doctor, Nurse, Hospital

class HospitalForm(ModelForm):
    """
    this is a user form used when updating user information
    """
    class Meta:
        model = Hospital
        fields = ['name', 'address']