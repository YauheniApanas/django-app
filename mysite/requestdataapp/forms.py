from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError


class UserBioForm(forms.Form):
    name = forms.CharField(max_length=25)
    age = forms.IntegerField(label='Your age', min_value=1, max_value=99)
    bio = forms.CharField(label='Biography', widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError('File name should not contain virus.')


def validate_file_size(file: InMemoryUploadedFile) -> None:
    if file and file.size > 10**6:
        raise ValidationError('File should not be more than 1MB.')


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name, validate_file_size])

