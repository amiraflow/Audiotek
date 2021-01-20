from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = "users"

urlpatterns = [
    path('', views.profile, name = "profil"),
    path('kolekcija/<username>', views.kolekcija, name = "kolekcija"),
    path('kolekcijaizv/<username>', views.kolekcijaizvodaci, name = "kolekcija izv"),
    path('kolekcijaalb/<username>', views.kolekcijaalbumi, name = "kolekcija alb"),
    path('kolekcijapj/<username>', views.kolekcijapjesme, name = "kolekcija pj"),
    #url('^login/$', "do_login", name='lastfmauth_login'),
    #url('^login_complete/$', "login_complete", name='lastfm_login_complete'),
    #path('lastlogin/', views.do_login, name='lastfmauth_login'),
    #path('lastlogin_complete/', views.login_complete, name='lastfm_login_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)