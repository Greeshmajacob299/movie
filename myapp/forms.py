from django import forms
from .models import *


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admintable
        fields = '__all__'

class CategoryForm(forms.ModelForm):
     class Meta:
        model = Genre
        fields = '__all__'


        
       