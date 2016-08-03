from django.contrib.auth.models import User
from django.forms import ModelForm
from models import *
from datetime import date
from django.forms.widgets import TextInput, Select
from django import forms
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

class CustomerForm(ModelForm):
    class Meta:
        model = Customers
        fields = ('location', 'name')

class MerchantForm(ModelForm):
    class Meta:
        model = Merchants
        fields = ('location', 'name','cost')

from django import forms
class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderForm(ModelForm):
    # docfile = forms.FileField(
    #     label='Select a file'
    # )
    # qty=forms.IntegerField()
    # date_of_order=forms.DateField()
    # date_of_delivery=forms.DateField()
    # customer = forms.ModelMultipleChoiceField(queryset=Customers.objects.all())
    # merchant = forms.ModelMultipleChoiceField(queryset=Merchants.objects.all())
    class Meta:
        model = Orders
        fields = ('qty','merchant','docfile')
        widgets = {
            'date_of_delivery': DateInput(),
        }
        exclude=('customer','completed','date_of_order','date_of_delivery')

class UpdateForm(ModelForm):
    class Meta:
        model=Merchants
        widgets = {'name':Select(attrs={'class': 'form-control'}),
                  'location':Select(attrs={'class': 'form-control'}),
                  'cost':Select(attrs={'class': 'form-control'})
                  }
        fields=('name','location','cost')