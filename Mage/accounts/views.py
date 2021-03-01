from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from accounts.models import *
#from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from accounts.forms import *
# Create your views here.

class EnteringView(ListView):
    model = Produs

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('produs_list')



    context = {'form': form}
    return render (request, 'accounts/register.html', context)


def Cosulet(request, pk,):
    item = Produs.objects.get(id=pk)
    item2 = Istoric()
    item2.autor = MyUser.objects.get(id=pk)
    item2.item = Produs.objects.get(id=pk)
    item.cantitate = item.cantitate - 1
    if item.cantitate <= 0:
        item.cantitate = 0
    item.save()
    item2.save()

    return render(request, 'accounts/cosulet.html', {'produs_list': item})
