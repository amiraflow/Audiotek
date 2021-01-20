from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
# Create your models here.

from users.models import Profile

class film(models.Model):
    ime_filma = models.CharField(max_length=500, default="")
    opis = models.TextField(default="")
    slika = models.ImageField(default = 'default.jpg', upload_to = 'kolekcija')
    zanr = models.CharField(max_length=500, default="")
    trajanje = models.CharField(max_length=500, default="")
    glumci = models.TextField(default="")
    redatelj = models.CharField(max_length=500, default="")
    trailer = models.TextField(default="")
    slajder = models.TextField(default="")

    def __str__(self):
        return self.ime_filma

class izvodac(models.Model):
    naziv = models.CharField(max_length=500, default="")
    #id = models.IntegerField()
    opis = models.TextField(default="", blank=True)
    slika = models.TextField(default="", blank=True)
    korisnik = models.ForeignKey(User, on_delete = models.CASCADE)
    lajkovi = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.naziv

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('kolekcija:Izvodac', args=[str(self.naziv)])

class album(models.Model):
    naziv = models.CharField(max_length=500, default="")
    izvodac = models.CharField(max_length=500, default="")
    opis = models.TextField(default="", blank=True)
    slika = models.TextField(default="", blank=True)
    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.naziv


class pjesma(models.Model):
    naziv = models.CharField(max_length=500, default="")
    izvodac = models.CharField(max_length=500, default="")
    opis = models.TextField(default="", blank=True)
    slika = models.TextField(default="", blank=True)
    korisnik = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.naziv