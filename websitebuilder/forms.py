from django import forms

class AIGeneratorForm(forms.Form):
    title = forms.CharField(max_length=100)
    business_type = forms.CharField(max_length=100)
    industry = forms.CharField(max_length=100)
