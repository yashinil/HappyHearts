from django import forms
from django.contrib.auth.models import User
 
class LenderForm(forms.Form):
    lender = forms.CharField()
    product_name = forms.CharField()
    product_description = forms.CharField()
    department=forms.CharField()
    safety_deposit=forms.IntegerField()
    contact_number=forms.IntegerField()
    image = forms.FileField()


'''

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')     

'''






