from django import forms
from django.core.exceptions import ValidationError


def only_int(value):
    if value.isdigit() == False:
        raise ValidationError("ID contains characters")


class SignUpForm(forms.Form):
    fullname = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    phone = forms.CharField(max_length=10, validators=[only_int])
    password = forms.CharField(max_length=50)
    occupation = forms.CharField(max_length=50)
    dob = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    address = forms.CharField(max_length=255)


class SignInForm(forms.Form):
    phone = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)


class NewPostForm(forms.Form):
    title = forms.CharField(max_length=200)
    body = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
