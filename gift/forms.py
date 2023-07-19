from django import forms

class GiftFinderForm(forms.Form):
    age = forms.IntegerField(label='Age',widget=forms.TextInput(attrs={'placeholder': 'Age'}))
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], widget=forms.RadioSelect)
    interests = forms.CharField(label='Interests',widget=forms.TextInput(attrs={'placeholder': 'Interests'}))


