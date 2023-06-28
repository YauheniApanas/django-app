from django import forms
from myauth.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class AboutForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
