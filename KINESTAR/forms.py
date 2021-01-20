
from django.contrib.auth.models import User
from django import forms
from users.models import Profile
from kolekcija.models import izvodac, pjesma, album

# nasljeđivanje iz ugrađenog modela modelform
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
#podaci o klasi
    class Meta:
        model = User
        fields = ['username','email','password']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']
        help_texts = {
            'username': None,
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'ime', 'prezime', 'adresa']
        labels = {
            'image': 'Slika',
        }


class IzvodacForm(forms.ModelForm):
    class Meta:
        model = izvodac
        fields = ['opis']

class PjesmaForm(forms.ModelForm):
    class Meta:
        model = pjesma
        fields = ['opis']

class AlbumForm(forms.ModelForm):
    class Meta:
        model = album
        fields = ['opis']

def should_be_empty(value):
    if value:
        raise forms.ValidationError('Polje nije prazno')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=80)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput, label="Ostavi prazno", validators=[should_be_empty])