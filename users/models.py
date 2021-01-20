from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# profil je povezan sa userom iz baze, ako se user briše briše se i profil
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_photos')
    ime = models.CharField(max_length=500, default="", blank=True)
    prezime = models.CharField(max_length=500, default="", blank=True)
    adresa = models.CharField(max_length=1000, default="", blank=True)


    def __str__(self):
        return f'{self.user.username} Profile'
