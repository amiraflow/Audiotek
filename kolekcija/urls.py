from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "kolekcija"

urlpatterns = [
    path('', views.IndexView.as_view(), name = "index"),
    path('kolekcija/', views.FilmoviIndexView.as_view(), name = "kolekcija-lista"),
    path('film/<pk>', views.FilmoviDetailView.as_view(), name="kolekcija-detail"),
    path('about/', views.about, name="about"),
    path('kontakt/', views.about, name="kontakt"),
    path('izvodac/<artist>', views.ispisijednog, name="Izvodac"),
    path('album/<mbid>', views.ispisijedanalbum, name = "AlbumMbid"),
    path('album/<izv>/<ime>', views.ispisijedanalbumpoimenu, name = "Album"),
    path('pjesma/<izvodac>/<pj>/', views.ispisijednupjesmu, name = "Pjesma"),
    path('tag/<imetaga>', views.ispisijedantag, name = "Tag"),
    path('toplistaizvodaca/', views.toplistaizvodaca, name="Top lista izvodaca"),
    path('toplistapjesama/', views.toplistapjesama, name="Top lista pjesama"),
    path('lokacija/', views.vidinalokaciji, name="Lokacija"),
    path('pretrazialbume/', views.pretrazialbume, name="Albumi"),
    path('pretrazipjesme/', views.pretrazipjesme, name="Pjesme"),
    path('pretraziizvodace/', views.pretraziizvodace, name="Izvodaci"),
    path('dodajizvodaca/<artist>/', views.dodajubazu, name="Dodaj_izvodaca"),
    path('dodajalbum/<izv>/<ime>', views.dodajubazualbum, name="Dodaj album"),
    path('dodajpjesmu/<izv>/<ime>', views.dodajubazupjesmu, name="Dodaj pjesmu"),
    path('izbrisi/<artist>', views.izbrisi, name="Izbrisi izvodaca"),
    path('izbrisialbum/<izv>/<ime>', views.izbrisialbum, name="Izbrisi album"),
    path('izbrisipjesmu/<izv>/<ime>', views.izbrisipjesmu, name="Izbrisi pjesmu"),
    path('dodan/', views.dodan, name="Dodan"),
    path('like/<artist>', views.like_izvodac, name="like_izvodac"),
    path('contact', views.contact, name="Kontakt"),
    path('uredi/<username>/<artist>', views.urediizvodaca, name = "urediizvodaca"),
    path('uredi/<username>/<izvodac>/<naziv>', views.uredipjesmu, name = "uredipjesmu"),
    path('uredialbum/<username>/<izvodac>/<nazivalbuma>', views.uredialbum, name = "uredialbum"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)