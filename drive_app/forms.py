from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from drive_app.models import Folder, File


class userregistrationform(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField(widget=forms.NumberInput)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        # Custom fields like phone and address need to be saved elsewhere, e.g., a profile model
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

# Form for uploading a file
class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']