from cProfile import label
from dataclasses import fields
from pyexpat import model
from turtle import title
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Document


# registration form
class user_registration(UserCreationForm):
    class Meta:
        model=User
        fields = ('username', 'password1','password2')
    def save(self,commit=True):
        user = super(user_registration, self).save(commit=False)
        if commit:
            user.save()
            return user


ROI_CHOISES = [
        ('enter','Select a Region'),
        ('Brainstem','Brainstem'),
        ('Chochlea R','Chochlea R'),
        ('Chochlea L','Chochlea L'),
        ('Dental Amalgam','Dental Amalgam'),
        ('GTV', 'GTV'),
        ('Lacrimal R','Lacrimal R'),
        ('Lens R','Lens R'),
        ('Optic Chiasm','Optic Chiasm'),
        ('Optic Nerve','Optic Nerve'),
        ('PTV', 'PTV'),
        ('Retina R', 'Retina R'),
        ('Teeth','Teeth')
    ]

INSTIUTION_CHOICES = [
    ('UCLA','UCLA'),
    ('SUNY B', 'SUNY B'),
    ('OTHERS','OTHERS')
]


# filter criteria table
class big_form(forms.Form):
    # roi selection
    roi = forms.CharField(label='Select ROI', widget=forms.Select(choices=ROI_CHOISES, attrs={'style':'width: 300px;','class': 'form-control'}), required=False)
    # institution
    institution = forms.CharField(label='Select Institution', widget=forms.CheckboxSelectMultiple    (choices=INSTIUTION_CHOICES),required=False)


# upload file form
class UploadForm(forms.ModelForm):
    uploadedFile = forms.FileField(label='Select a DICOM file to upload')
    class Meta:
        model=Document
        fields=('uploadedFile',)