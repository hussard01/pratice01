'''
Created on 2014. 12. 9.

@author: user
'''

from django import forms
from redactor.widgets import RedactorEditor

class writeForm(forms.Form):
    content = forms.CharField(widget=RedactorEditor())

class loginForm(forms.Form):
    name =  forms.CharField(min_length=2, max_length=20)
    password = forms.CharField(min_length=2, max_length=20)

class joinForm(forms.Form):
    name = forms.CharField(min_length=2, max_length=20)
    email =  forms.CharField(min_length=2, max_length=20)
    password = forms.CharField(min_length=2, max_length=20)
    password2 = forms.CharField(min_length=2, max_length=20)

class NameForm(forms.Form):
    pass

    