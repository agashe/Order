from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField(required=True, min_length=8)

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField(required=True, min_length=8)
    confirm = forms.CharField(required=True, min_length=8)

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField(required=True, min_length=8)
    confirm = forms.CharField(required=True, min_length=8)
