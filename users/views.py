from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from KINESTAR.forms import UserUpdateForm, ProfileUpdateForm
from django.conf import settings
from .models import Profile
from django.contrib.auth.models import User
from kolekcija.models import izvodac, album, pjesma

API_KEY = settings.LASTFM_API_KEY



# Create your views here.
#@login_required
def profile(request):
    profil = Profile.objects.get(user=User.objects.get(username=request.user.username))
    ime = profil.ime
    prezime = profil.prezime
    adresa = profil.adresa
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users:profil')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'ime': ime,
        'prezime': prezime,
        'adresa': adresa,
    }

    return render(request, 'users/profil.html', context)

def kolekcija(request, username):
    profil = Profile.objects.get(user=User.objects.get(username=username))
    ime = profil.ime
    prezime = profil.prezime
    adresa = profil.adresa
    izvodaci = izvodac.objects.filter(korisnik=User.objects.get(username=username))[:3]
    albumi = album.objects.filter(korisnik=User.objects.get(username=username))[:3]
    pjesme = pjesma.objects.filter(korisnik=User.objects.get(username=username))[:3]
    context = {
        'izvodacs': izvodaci,
        'albums': albumi,
        'pjesmas': pjesme,
        'p_form': 'ime',
        'ime': ime,
        'prezime': prezime,
        'adresa': adresa,
        'kor': username,
    }

    return render(request, 'users/kolekcija.html', context)

def kolekcijaizvodaci(request, username):
    profil = Profile.objects.get(user=User.objects.get(username=username))
    ime = profil.ime
    prezime = profil.prezime
    adresa = profil.adresa
    izvodaci = izvodac.objects.filter(korisnik=User.objects.get(username=username))
    rijec = "Izvođači"
    context = {
        'rijec': rijec,
        'izvodacs': izvodaci,
        'p_form': 'ime',
        'ime': ime,
        'prezime': prezime,
        'adresa': adresa,
        'kor': username,
    }

    return render(request, 'users/kolekcijadetaljno.html', context)

def kolekcijaalbumi(request, username):
    profil = Profile.objects.get(user=User.objects.get(username=username))
    ime = profil.ime
    prezime = profil.prezime
    adresa = profil.adresa
    albumi = album.objects.filter(korisnik=User.objects.get(username=username))
    rijec = "Albumi"
    context = {
        'rijec': rijec,
        'izvodacs': albumi,
        'p_form': 'ime',
        'ime': ime,
        'prezime': prezime,
        'adresa': adresa,
        'kor': username,
    }

    return render(request, 'users/kolekcijadetaljno.html', context)

def kolekcijapjesme(request, username):
    profil = Profile.objects.get(user=User.objects.get(username=username))
    ime = profil.ime
    prezime = profil.prezime
    adresa = profil.adresa
    pjesme = pjesma.objects.filter(korisnik=User.objects.get(username=username))
    rijec = "Pjesme"
    context = {
        'rijec': rijec,
        'izvodacs': pjesme,
        'p_form': 'ime',
        'ime': ime,
        'prezime': prezime,
        'adresa': adresa,
        'kor': username,
    }

    return render(request, 'users/kolekcijadetaljno.html', context)

