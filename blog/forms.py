'''
Created on 2014. 12. 9.

@author: user
'''

from django import forms
from redactor.widgets import RedactorEditor

class writeForm(forms.Form):
    content = forms.CharField(widget=RedactorEditor())
    

class NameForm(forms.Form):
    pass

    