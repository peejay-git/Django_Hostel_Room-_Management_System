from dataclasses import field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.forms import ModelForm
from django import forms
from .models import Complain



class DateInput(forms.DateInput):
    input_type = 'date'

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ('category','subject','complain_start_date','date_reported', 'desc')
        widgets = {
            'complain_start_date': DateInput(),
            'date_reported': DateInput(),
        }

class SAComplaintForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ('is_attended',)




# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email')
        
