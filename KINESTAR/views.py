from django.views import generic
from django.views.generic import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
from django.http import HttpResponse


class UserFormView(View):
    form_class = UserForm
    template_name = 'registration/registration_form.html'

# kad se tek otvori stranica, pošalje se get request i učita mu se htlm
    def get(self, request):
        form = self.form_class(None) # forma inicijalno nema podatke
        return render(request, self.template_name, {'form': form})

# kad korisnik ispuni formu i pošalje nešto
    def post(self, request):
        form = self.form_class(request.POST) # forma se ispuni podacima iz POST metode

        if form.is_valid():
            user = form.save(commit = False)

            # normalizirani podaci
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # vrati korisnika ako su ispravni podaci
            user = authenticate(username = username, password = password)

            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect('kolekcija:index')

        return redirect('kolekcija:index')

def about(request):
    return HttpResponse('o nama')