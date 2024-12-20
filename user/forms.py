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
    phone = forms.CharField(max_length=200, required=True)
    country = forms.CharField(max_length=200, required=True)
    state = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=200, required=True)
    details = forms.CharField(max_length=200, required=True)
    postcode = forms.CharField(max_length=200, required=False)
    # old_password = forms.CharField(required=False, min_length=8)
    # new_password = forms.CharField(required=False, min_length=8)
    # confirm = forms.CharField(required=False, min_length=8)
