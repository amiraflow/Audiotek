# Generated by Django 3.1 on 2020-10-04 01:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime_filma', models.CharField(default='', max_length=500)),
                ('opis', models.TextField(default='')),
                ('slika', models.ImageField(default='default.jpg', upload_to='kolekcija')),
                ('zanr', models.CharField(default='', max_length=500)),
                ('trajanje', models.CharField(default='', max_length=500)),
                ('glumci', models.TextField(default='')),
                ('redatelj', models.CharField(default='', max_length=500)),
                ('trailer', models.TextField(default='')),
                ('slajder', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='pjesma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(default='', max_length=500)),
                ('izvodac', models.CharField(default='', max_length=500)),
                ('opis', models.TextField(blank=True, default='')),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='izvodac',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(default='', max_length=500)),
                ('opis', models.TextField(blank=True, default='')),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naziv', models.CharField(default='', max_length=500)),
                ('izvodac', models.CharField(default='', max_length=500)),
                ('opis', models.TextField(blank=True, default='')),
                ('korisnik', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
