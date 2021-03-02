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
    template_name = "accounts/home_list.html"
    model = Product

class LoginView(ListView):
    template_name = "registration/login.html"
    model = Product

def succes_view(request):
    return render(request, "accounts/succes_login.html")

def registerPage(request):
    form = CreateUserForm()
    messages = []
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            messages.append("Inregistrare cu success")
            context = {"messages": messages}
            form.save()
            return render(request, "accounts/register.html", context)

    context = {'form': form}
    return render (request, 'accounts/register.html', context)


def HistoryDetail(request, pk):
    item = Product.objects.get(id=pk)
    item2 = History()
    print(request.user)

    item2.author = MyUser.objects.get(pk=request.user.pk)
    item2.item = Product.objects.get(id=pk)
    item.quantity = item.quantity - 1
    if item.quantity <= 0:
        item.quantity = 0
    item.save()
    item2.save()

    return render(request, 'accounts/basket.html', {'item': item})
