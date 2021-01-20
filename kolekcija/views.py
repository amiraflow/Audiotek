from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
import json
from KINESTAR.settings import USER_AGENT, LASTFM_API_KEY
from KINESTAR.forms import IzvodacForm, ContactForm, PjesmaForm, AlbumForm
from .models import film, izvodac, album, pjesma
from django.urls import reverse_lazy, NoReverseMatch
from django.views import generic, View
from django.views.generic import CreateView, DeleteView, UpdateView, RedirectView
import requests
from django.conf import settings
import requests_cache
import time
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from .models import izvodac, pjesma, album

requests_cache.install_cache()

def getsliku(izvodac):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="db2fdc2f9bb74b21bdb00c5c8ffab8c1",
                                                               client_secret="382d091a0d354a1b8f60519161df5564"))


    ispis = sp.search(q=izvodac, limit=1, type='artist')
    try:
        slika = ispis['artists']['items'][0]['images'][0]['url']
    except:
        slika = "https://fashionista.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cg_faces:center%2Cq_auto:good%2Cw_620/MTU2NDk0ODQ4MjY0Nzc0NzQ3/harry-styles-gucci-madison-square-garden-th.jpg"


    return slika

def getslikupjesme(pjesma):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="db2fdc2f9bb74b21bdb00c5c8ffab8c1",
                                                               client_secret="382d091a0d354a1b8f60519161df5564"))


    ispis = sp.search(q=pjesma, limit=1, type='track')
    #jprint(sp.search(q=varijabla, limit=1, type='track'))
    try:
        slika = ispis['tracks']['items'][0]['album']['images'][0]['url']
    except:
        slika = "https://fashionista.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cg_faces:center%2Cq_auto:good%2Cw_620/MTU2NDk0ODQ4MjY0Nzc0NzQ3/harry-styles-gucci-madison-square-garden-th.jpg"


    return slika

def getslikupjesmeizv(pjesma, izvodac):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="db2fdc2f9bb74b21bdb00c5c8ffab8c1",
                                                               client_secret="382d091a0d354a1b8f60519161df5564"))


    ispis = sp.search(q='artist:{} track:{}'.format(izvodac, pjesma), limit=1, type='track')
    #jprint(sp.search(q=varijabla, limit=1, type='track'))
    try:
        slika = ispis['tracks']['items'][0]['album']['images'][0]['url']
    except:
        slika = "https://fashionista.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cg_faces:center%2Cq_auto:good%2Cw_620/MTU2NDk0ODQ4MjY0Nzc0NzQ3/harry-styles-gucci-madison-square-garden-th.jpg"


    return slika




def about(request):
    return render(request, 'about.html', {'title': 'O nama'})

def kontakt(request):
    return render(request, 'kontakt.html', {'title': 'Kontakt'})

class IndexView(View):
    def get(self, request):
        context = {'svi_filmovi' : film.objects.all}
        return render(request, 'index.html', context)

class FilmoviIndexView(generic.ListView):
    template_name = 'filmovi/filmoviindex.html'

    def get_queryset(self):
        return film.objects.all()

class FilmoviDetailView(generic.DetailView):
    model = film
    template_name = 'filmovi/detail.html'


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def lookup_tags(artist):
    response = lastfm_get({
        'method': 'artist.getTopTags',
        'artist':  artist
    })

    # if there's an error, just return nothing
    if response.status_code != 200:
        return None

    # extract the top three tags and turn them into a string
    tags = [t['name'] for t in response.json()['toptags']['tag'][:3]]
    tags_str = ', '.join(tags)

    # rate limiting
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)
    return tags_str

def lastfm_artist_search(request):
    api_url = 'http://ws.audioscrobbler.com/2.0/'
    api_key = settings.LASTFM_API_KEY
    url = api_url+'?method=artist.search&format=json&artist='+'Muse'+'&api_key='+api_key
    data = requests.get(url)
    return render(request, 'index.html', data.text)


def izvodaciSTARO(request):
    videos = []

    if request.method == 'POST':
        search_url = 'http://ws.audioscrobbler.com/2.0/?method=artist.search&format=json'
        #video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'limit': 9,
            'artist': request.POST['search'],
            'api_key': settings.LASTFM_API_KEY
        }

        r = requests.get(search_url, params=search_params)
        print(r.json()['results']['artistmatches']['artist'][0]['name'])
        results = ['results']
        print(results)


        for result in results:
            videos.append(result['artistmatches']['artist'][0]['name'])

    context = {
        'videos': videos
    }

    return render(request, 'toplista.html', context)

def lastfm_get(payload):
    # definiranje headera i url-a
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # dodavanje ključa i formata 
    payload['api_key'] = LASTFM_API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def toplistaizvodaca(request):
    r = lastfm_get({
        'method': 'chart.gettopartists',
        'limit': 15
    })

    r.status_code

    #jprint(r.json())
    rezultats = r.json()['artists']['artist']

    listas = []
    i = 1;
    for rezultat in rezultats:
        slika = getsliku(rezultat['name'])
        podaci = {
            'broj': i,
            'naziv': rezultat['name'],
            'listeners': rezultat['listeners'],
            "mbid": rezultat['mbid'],
            "playcount": rezultat['playcount'],
            "tags": lookup_tags(rezultat['name']),
            "slika": slika,
        }
        i=i+1;
        listas.append(podaci)

    #print(r.json()['artists']['artist'][0]['name'])
    print(listas)

    context = {
        'listas': listas
    }
    return render(request, 'toplista.html', context)

@login_required()
def ispisijednog(request, artist):
    r = lastfm_get({
    'method': 'artist.getInfo',
    'artist': artist,
    })

    print(r.status_code)

    jprint(r.json())

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="db2fdc2f9bb74b21bdb00c5c8ffab8c1",
                                                                   client_secret="382d091a0d354a1b8f60519161df5564"))

    ispis = sp.search(q=artist, limit=1, type='artist')
    slika = ispis['artists']['items'][0]['images'][0]['url']
        #jprint(ispis)
        #jprint(slika)

    baza = False
    rezultat = r.json()['artist']
    slicniizvodaci = [t['name'] for t in rezultat['similar']['artist'][:5]]
    slicnis = [t['name'] for t in rezultat['similar']['artist'][:5]]
    slike = []
    for slicni in slicnis:
        slike.append(getsliku(slicni))



    tagovi = [r['name'] for r in rezultat['tags']['tag'][:3]]
    provjera = izvodac.objects.filter(korisnik=request.user, naziv=rezultat['name'])
    if provjera.exists():
        baza = True
        print("Ima ga")


    opis = rezultat['bio']['summary']
    pozicija = opis.find("<a")
    print(pozicija)
    izrezani = opis[0:pozicija]
    lajkan = False

    try:
        izv = get_object_or_404(izvodac, naziv=rezultat['name'])
        niz = izv.lajkovi.filter(id=request.user.id)
        print(niz)
        if(not(niz)):
            lajkan = False
        else:
            lajkan = True
    except:
        lajkan = False
    #provjera2 = izvodac.objects.filter(korisnik=request.user, naziv=rezultat['name'], lajkovi__username=request.user.username)
    #if provjera2:
     #   lajkan = True

    podaci = {
        'lajkan': lajkan,
         'slika': slika,
         'naziv': rezultat['name'],
         'bio': rezultat['bio']['content'],
        'summary': izrezani,
         #'mbid': rezultat['mbid'],
        'ontour': rezultat['ontour'],
        'listeners': rezultat['stats']['listeners'],
        'plays': rezultat['stats']['playcount'],
        'slicni': slicniizvodaci,
        'tags': tagovi,
        'baza': baza,
        'slike': slike,
    }



    # print(r.json()['artists']['artist'][0]['name'])
    jprint(podaci)


    context = {
    'podaci': podaci
     }

    return render(request, 'izvodac.html', context)



@login_required()
def ispisijedanalbum(request, mbid):

    r = lastfm_get({
        'method': 'album.getInfo',
        'mbid': mbid,
    })

    print(r.status_code)

    #jprint(r.json())

    rezultat = r.json()['album']
    tags = [t['name'] for t in rezultat['tags']['tag'][:5]]
    pjesme = [p['name'] for p in rezultat['tracks']['track'][:20]]
    baza = False
    provjera = album.objects.filter(korisnik=request.user, naziv=rezultat['name'], izvodac=rezultat['artist'])
    if provjera.exists():
        baza = True
        print("Ima ga")

    podaci = {
        'baza': baza,
        'naziv': rezultat['name'],
        'izvodac': rezultat['artist'],
        'slika': rezultat['image'][3]['#text'],
        'listeners': rezultat['listeners'],
        'mbid': rezultat['mbid'],
        'plays': rezultat['playcount'],
        'dugiopis': rezultat['wiki']['content'],
        'kratkiopis': rezultat['wiki']['summary'],
        'objavljen': rezultat['wiki']['published'],
        'tagovi': tags,
        'pjesme': pjesme,
    }
    #    "mbid": "1dad9b13-1f02-33f6-815e-7fb2e6af17ea"
    context = {
        'podaci': podaci
    }
    return render(request, 'album.html', context)

@login_required()
def ispisijedanalbumpoimenu(request, izv, ime):
    try:
        r = lastfm_get({
            'method': 'album.getInfo',
            'artist': izv,
            'album': ime,
        })

        print(r.status_code)

        jprint(r.json())

        rezultat = r.json()['album']
        tags = [t['name'] for t in rezultat['tags']['tag'][:5]]
        pjesme = [p['name'] for p in rezultat['tracks']['track'][:20]]
        try:
            opis = rezultat['wiki']['summary']
        except KeyError:
            opis = "Podaci nedostupni"

        pozicija = opis.find("<a")
        print(pozicija)
        izrezani = opis[0:pozicija]
        baza = False
        provjera = album.objects.filter(korisnik=request.user, naziv=rezultat['name'], izvodac=rezultat['artist'])
        if provjera.exists():
            baza = True
            print("Ima ga")
        podaci = {
            'baza': baza,
            'naziv': rezultat['name'],
            'izvodac': rezultat['artist'],
            'slika': rezultat['image'][3]['#text'],
            'listeners': rezultat['listeners'],
            # 'mbid': rezultat['mbid'],
            'plays': rezultat['playcount'],
            # 'dugiopis': rezultat['wiki']['content'],
            'kratkiopis': izrezani,
            # 'objavljen': rezultat['wiki']['published'],
            'tagovi': tags,
            'pjesmas': pjesme,
        }
        #    "mbid": "1dad9b13-1f02-33f6-815e-7fb2e6af17ea"
        context = {
            'podaci': podaci
        }
        return render(request, 'album.html', context)
    except NoReverseMatch:
        podaci = {
            'baza': baza,
            'naziv': "Nedostupan album",
            'izvodac': "Nedostupan album",
            'slika': "Nedostupan album",
            'listeners': "Nedostupan album",
            # 'mbid': rezultat['mbid'],
            'plays': "Nedostupan album",
            # 'dugiopis': rezultat['wiki']['content'],
            'kratkiopis': "Nedostupan album",
            # 'objavljen': rezultat['wiki']['published'],
            'tagovi': "Nedostupan album",
            'pjesmas': "Nedostupan album",
        }
        #    "mbid": "1dad9b13-1f02-33f6-815e-7fb2e6af17ea"
        context = {
            'podaci': podaci
        }
        return render(request, 'album.html', context)


@login_required()
def ispisijednupjesmu(request, izvodac, pj):
    r = lastfm_get({
        'method': 'track.getInfo',
        'artist': izvodac,
        'track': pj,
    })

    print(r.status_code)
    rezultat = r.json()['track']
    tags = [t['name'] for t in rezultat['toptags']['tag'][:5]]
    #jprint(r.json())
    album = "Nedostupan"
    slika = "Nedostupna"
    try:
        album = rezultat['album']['title']
        slika = rezultat['album']['image'][3]['#text'],
        opis = rezultat['wiki']['summary']
    except KeyError:
        album = "Nedostupan"
        opis = "Podaci nedostupni"
        slika = "Podaci nedostupini"

    pozicija = opis.find("<a")
    print(pozicija)
    izrezani = opis
    if pozicija != (-1):
        izrezani = opis[0:pozicija]
    baza = False
    provjera = pjesma.objects.filter(korisnik=request.user, naziv=rezultat['name'], izvodac=rezultat['artist']['name'])
    if provjera.exists():
        baza = True
        print("Ima ga")
    podaci = {
        'baza': baza,
        'naziv': rezultat['name'],
        'album': album,
        #'mbidalbuma': rezultat['album']['mbid'],
        #'pozicija': rezultat['album']['@attr']['position'],
        'izvodac': rezultat['artist']['name'],
        'slikaizvodaca': getsliku(rezultat['artist']['name']),
        #'mbidizvodaca': rezultat['artist']['mbid'],
        'slika': slika,
        'trajanje': rezultat['duration'],
        'listeners': rezultat['listeners'],
        #'mbidpjesme': rezultat['mbid'],
        'plays': rezultat['playcount'],
        #'mbid': rezultat['mbid'],
        'kratkiopis': izrezani,
        'tagovi': tags,
    }

    jprint(podaci)
    context = {
        'podaci': podaci
    }

#0164a138-ca8a-4d0c-bd90-2cb1285b88a3

    return render(request, 'pjesma.html', context)

@login_required()
def ispisijedantag(request, imetaga):
    r = lastfm_get({
        'method': 'tag.getInfo',
        'tag': imetaga,
    })

    print(r.status_code)
    rezultat = r.json()['tag']
    #jprint(r.json())
    r2 = lastfm_get({
        'method': 'tag.getTopAlbums',
        'tag': imetaga,
        'limit': 10
    })
    rezultat2s = r2.json()['albums']['album']
    topalbums = []
    i=1;
    for rezultat2 in rezultat2s:
        podacialbumi = {
            'broj': i,
            'naziv': rezultat2['name'],
            'mbid': rezultat2['mbid'],
            'izvodac': rezultat2['artist']['name'],
            'mbidizvodaca': rezultat2['artist']['mbid'],
            'slika': rezultat2['image'][3]['#text'],
        }
        i = i+1
        topalbums.append(podacialbumi)

    r3 = lastfm_get({
        'method': 'tag.getTopArtists',
        'tag': imetaga,
        'limit': 5,
    })

    #jprint(r3.json())
    rezultat3s = r3.json()['topartists']['artist']
    j = 1;
    topartists = []
    for rezultat3 in rezultat3s:
        podaciizvodaci = {
            'broj': i,
            'naziv': rezultat3['name'],
            'slika': getsliku(rezultat3['name']),
            #'mbidizvodaca': rezultat3['mbid']
            }
        j=j+1
        topartists.append(podaciizvodaci)
    opis = rezultat['wiki']['content']
    pozicija = opis.find("<a")
    print(pozicija)
    izrezani = opis[0:pozicija]
    podaci = {
        'naziv': rezultat['name'],
        'reach': rezultat['reach'],
        'total': rezultat['total'],
        'kratkiopis': izrezani,
        'dugiopis': izrezani,
        'topalbums': topalbums,
        'topartists': topartists,
    }
    jprint(podaci)
#0164a138-ca8a-4d0c-bd90-2cb1285b88a3
    context = {
        'podaci': podaci
    }
    return render(request, 'tag.html', context)


def toplistapjesama(request):
    r = lastfm_get({
        'method': 'chart.getTopTracks',
        'limit': 15
    })


    jprint(r.json())
    rezultats = r.json()['tracks']['track']
    i = 1
    songs = []
    for rezultat in rezultats:
        podaci = {
            'broj': i,
            'naziv': rezultat['name'],
            "playcount": rezultat['playcount'],
            'izvodac': rezultat['artist']['name'],
            #"mbid": rezultat['mbid'],
            'slika': getslikupjesme(rezultat['name']),
        }
        i=i+1
        songs.append(podaci)


    print(songs)

    context = {
        'songs': songs
    }
    return render(request, 'toplistapjesama.html', context)




def vidinalokaciji(request):
    artists = []
    provjera = False;
    if request.method == 'POST':
        provjera = True;
        r = lastfm_get({
            'method': 'geo.getTopArtists',
            'country': request.POST['search'],
            'limit': 9,
        })

        jprint(r.json())
        rezultats = r.json()['topartists']['artist']
        if request.POST['submit'] == 'lucky':
            return ispisijednog(request, r.json()['topartists']['artist'][0]['name'])

        for rezultat in rezultats:
            podaci = {
                'naziv': rezultat['name'],
                "listeners": rezultat['listeners'],
                #"mbid": rezultat['mbid'],
                "slika": getsliku(rezultat['name']),
            }

            artists.append(podaci)


    context = {
        'artists': artists,
        'provjera': provjera,
    }

    return render(request, 'lokacija.html', context)

def pretrazialbume(request):
    albums = []
    provjera = False;
    if request.method == 'POST':
        provjera = True;
        r = lastfm_get({
            'method': 'album.search',
            'album': request.POST['search'],
            'limit': 15,
        })

        jprint(r.json())
        rezultats = r.json()['results']['albummatches']['album']

        for rezultat in rezultats:
            podaci = {
                'naziv': rezultat['name'],
                'izvodac': rezultat['artist'],
                'mbid': rezultat['mbid'],
                'slika': rezultat['image'][3]['#text']
            }

            albums.append(podaci)
        if request.POST['submit'] == 'lucky':
            return ispisijedanalbumpoimenu(request, r.json()['results']['albummatches']['album'][0]['name'], r.json()['results']['albummatches']['album'][0]['artist'])

    context = {
        'albums': albums,
        'provjera': provjera,
    }

    return render(request, 'pretrazialbume.html', context)


def pretrazipjesme(request):
    tracks = []
    provjera = False;
    if request.method == 'POST':
        provjera = True;
        r = lastfm_get({
            'method': 'track.search',
            'track': request.POST['search'],
            'limit': 15,
        })

        jprint(r.json())
        rezultats = r.json()['results']['trackmatches']['track']

        for rezultat in rezultats:
            podaci = {
                'naziv': rezultat['name'],
                'izvodac': rezultat['artist'],
                'mbid': rezultat['mbid'],
                'listeners': rezultat['listeners'],
                'slika': getslikupjesmeizv(rezultat['name'], rezultat['artist']),
            }

            tracks.append(podaci)

        if request.POST['submit'] == 'lucky':
            return ispisijednupjesmu(request, r.json()['results']['trackmatches']['track'][0]['artist'], r.json()['results']['trackmatches']['track'][0]['name'])
    context = {
        'tracks': tracks,
        'provjera': provjera,
    }

    return render(request, 'pretrazipjesme.html', context)


def pretraziizvodace(request):
    artists = []  # prazan niz na izvođače
    provjera = False;
    # ako korisnik klikne na Pretraži, pozove se funkcija lastfm_get
    if request.method == 'POST':
        provjera = True;
        r = lastfm_get({
            'method': 'artist.search', # metoda artist.search
            'artist': request.POST['search'], # izvođač iz forme
            'limit': 9, # ispis prvih 9 izvođača
        })
        # spremanje dobijenih podataka u varijablu
        rezultats = r.json()['results']['artistmatches']['artist']
        # preusmjeravanje na prvog izvođača u nizu ako je korisnik odabrao da se osjeća sretno
        if request.POST['submit'] == 'lucky':
            naziv = r.json()['results']['artistmatches']['artist'][0]['name']
            return ispisijednog(request, naziv)
        # prijenos varijabli u HTML template
        for rezultat in rezultats:
            podaci = {
                'naziv': rezultat['name'],
                'mbid': rezultat['mbid'],
                'listeners': rezultat['listeners'],
                'slika': getsliku(rezultat['name'])
            }

            artists.append(podaci)
    context = {
        'artists': artists,
        'provjera': provjera,
    }

    return render(request, 'pretraziizvodace.html', context)

def dodan(request):
    return render(request, 'obrisano.html', {'title': 'Kontakt'})

@login_required
def dodajubazu(request, artist):
    print(artist)
    r = lastfm_get({
        'method': 'artist.getInfo',
        'artist': artist,
    })

    print(r.status_code)

    jprint(r.json())

    rezultat = r.json()['artist']
    jprint(rezultat)
    opis = rezultat['bio']['summary']
    pozicija = opis.find("<a")
    print(pozicija)
    izrezani = opis[0:pozicija]
    noviizvodac = izvodac()
    noviizvodac.naziv = rezultat['name']
    noviizvodac.opis = izrezani
    noviizvodac.slika = getsliku(rezultat['name'])
    noviizvodac.korisnik = request.user

    print('da')
    noviizvodac.save()
    context = {
        'izvodac': artist,
    }
    return render(request, 'dodano.html', context)

@login_required()
def izbrisi(request, artist):
    izvodac.objects.filter(naziv=artist, korisnik=request.user).delete()
    context = {
        'izvodac': artist,
    }
    return render(request, 'obrisano.html', context)

@login_required()
def dodajubazualbum(request, izv, ime):
    r = lastfm_get({
        'method': 'album.getInfo',
        'album': ime,
        'artist': izv,
    })

    rezultat = r.json()['album']
    jprint(rezultat)
    opis = rezultat['wiki']['summary']
    pozicija = opis.find("<a")
    print(pozicija)
    izrezani = opis[0:pozicija]
    novialbum = album()
    novialbum.naziv = rezultat['name']
    novialbum.izvodac = rezultat['artist']
    novialbum.opis = izrezani
    novialbum.slika = rezultat['image'][3]['#text']
    novialbum.korisnik = request.user

    print('da')
    novialbum.save()
    context = {
        'album': rezultat['name'],
        'izvodac': rezultat['artist'],
    }
    return render(request, 'dodanoalb.html', context)


@login_required()
def dodajubazupjesmu(request, izv, ime):

    r = lastfm_get({
        'method': 'track.getInfo',
        'track': ime,
        'artist': izv,
    })

    rezultat = r.json()['track']
    jprint(rezultat)
    opis = rezultat['wiki']['summary']
    pozicija = opis.find("<a")
    print(pozicija)
    izrezani = opis[0:pozicija]
    novialbum = pjesma()
    novialbum.naziv = rezultat['name']
    novialbum.izvodac = rezultat['artist']['name']
    novialbum.opis = izrezani
    novialbum.slika = getslikupjesmeizv(rezultat['name'], rezultat['artist']['name'])
    novialbum.korisnik = request.user

    print('da')
    novialbum.save()
    context = {
        'pjesma': rezultat['name'],
        'izvodac': rezultat['artist']['name'],
    }
    return render(request, 'dodanopj.html', context)

@login_required()
def izbrisialbum(request, izv, ime):
    album.objects.filter(naziv=ime, izvodac=izv, korisnik=request.user).delete()
    context = {
        'izvodac': izv,
        'album': ime,
    }
    return render(request, 'obrisanoalb.html', context)

def izbrisipjesmu(request, izv, ime):
    pjesma.objects.filter(naziv=ime, izvodac=izv, korisnik=request.user).delete()
    context = {
        'izvodac': izv,
        'album': ime,
    }
    return render(request, 'obrisanopj.html', context)

@login_required()
def like_izvodac(request, artist):
    try:
        izv = get_object_or_404(izvodac, naziv=artist)

        if izv.lajkovi.filter(id=request.user.id).exists():
            izv.lajkovi.remove(request.user.id)

        else:
            izv.lajkovi.add(request.user.id)

        return redirect("kolekcija:Izvodac", artist=artist)

    except:
        return redirect("kolekcija:Izvodac", artist=artist)


def contact(request):
    if request.method == 'POST':
        message_name = request.POST['message_name']
        message_email = request.POST['message_email']
        message = request.POST['message']
        message_subject = request.POST['message_subject']

        recipients = ['amira.midzic@gmail.com']
        try:
            send_mail(message_subject, message, message_email, recipients, fail_silently=True)
        except BadHeaderError:
            poruka = "E-mail nije poslan"
            return render(request, 'contact.html', {'poruka': poruka})


        poruka = "E-mail poslan"
        return render(request, 'contact.html', {'poruka': poruka})
    else:
        poruka = ""
    return render(request, 'contact.html', {'poruka': poruka})
@login_required()
def urediizvodaca(request, username, artist):
    if request.method == 'POST':
        forma = IzvodacForm(request.POST, instance=izvodac.objects.get(naziv=artist, korisnik=User.objects.get(username=username)))
        print(izvodac.objects.get(naziv=artist))
        if forma.is_valid():
            forma.save()
            messages.success(request, f'Izvođač u kolekciji uređen!')
            return redirect('kolekcija:urediizvodaca', username, artist)

    else:
        forma = IzvodacForm(instance=izvodac.objects.get(naziv=artist, korisnik=User.objects.get(username=username)))

    context = {
        'forma': forma,
    }

    return render(request, 'uredi.html', context)

@login_required()
def uredipjesmu(request, username, izvodac, naziv):
    if request.method == 'POST':
        forma = PjesmaForm(request.POST, instance=pjesma.objects.get(naziv=naziv, izvodac = izvodac, korisnik=User.objects.get(username=username)))
        print(pjesma.objects.get(naziv=naziv, izvodac=izvodac))
        if forma.is_valid():
            forma.save()
            messages.success(request, f'Pjesma u kolekciji uređena!')
            return redirect('users:kolekcija', username)

    else:
        forma = PjesmaForm(instance=pjesma.objects.get(naziv=naziv, izvodac=izvodac, korisnik=User.objects.get(username=username)))

    context = {
        'forma': forma,
    }

    return render(request, 'uredi.html', context)

@login_required()
def uredialbum(request, username, izvodac, nazivalbuma):
    if request.method == 'POST':
        forma = AlbumForm(request.POST, instance=album.objects.get(naziv=nazivalbuma, izvodac = izvodac, korisnik=User.objects.get(username=username)))

        if forma.is_valid():
            forma.save()
            messages.success(request, f'Album u kolekciji uređen!')
            return redirect('users:kolekcija', username)

    else:
        forma = AlbumForm(instance=album.objects.get(naziv=nazivalbuma, izvodac=izvodac, korisnik=User.objects.get(username=username)))

    context = {
        'forma': forma,
    }

    return render(request, 'uredi.html', context)