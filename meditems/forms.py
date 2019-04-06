from django import forms
from django.forms import ModelForm
from meditems.models import Prescription, Test, MedicalNote


class PrescriptionForm(ModelForm):
    """
    this form is used to create prescriptions
    """

    class Meta:
        model = Prescription
        fields = ["patient", "name", "dosage", "refills", "doc"]
        exclude = ["doc"]


class TestForm(ModelForm):
    """
    this form is used to create test results
    """
    class Meta:
        model = Test
        fields = ["patient", "name", "comments", "doc", "released", "file"]
        exclude = ["doc"]

class MedicalNoteForm(ModelForm):
    """
    this form is used to create medical notes
    """
    class Meta:
        model = MedicalNote
        fields = ["patient","doctor","note"]

    note = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "50", 'rows': "4","height":"20%" ,"style":"resize:none;"}))



