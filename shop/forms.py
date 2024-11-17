from django import forms

class CheckoutForm(forms.Form):
    phone = forms.CharField(max_length=200, required=True)
    country = forms.CharField(max_length=200, required=True)
    state = forms.CharField(max_length=200, required=True)
    city = forms.CharField(max_length=200, required=True)
    details = forms.CharField(max_length=200, required=True)
    postcode = forms.CharField(max_length=200, required=False)
    notes = forms.CharField(max_length=500, required=False)
