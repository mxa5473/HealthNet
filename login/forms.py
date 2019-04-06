from django import forms

from account.models import Patient
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User = get_user_model()


class UserLoginForm(forms.Form):
    """
    This form is used for user login
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:

            user = authenticate(username=username, password=password)

            user_qs = User.objects.filter(username=username)

            if user_qs.count() == 1:
                user = user_qs.first()

            if not user:
                raise forms.ValidationError("This user does not exist")

            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")

            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")

            return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    """
    This form is a registration form for PATIENTS ONLY
    """
    email = forms.EmailField(label="Confirm Email")
    email2 = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(label="First Name", max_length=20)
    last_name = forms.CharField(label="Last Name", max_length=20)

    class Meta:
        model = User
        fields = [
            'username',
            'email2',
            'email',
            'first_name',
            'last_name',
            'password'

        ]

    def clean_email(self):
        """
        Tests if email has already been registered or if the provided
        emails do not match
        """
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")

        email_qs = User.objects.filter(email=email)

        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")

        return email


