from django import forms

class SubscribeForm(forms.Form):
    email = forms.EmailField(max_length=200, required=True)

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=200, required=True)
    body = forms.CharField(required=True)
