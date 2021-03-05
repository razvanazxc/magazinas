from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from accounts.models import *
import secrets
from django.core.mail import send_mail
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
        token = secrets.token_hex(5)

        form = CreateUserForm(request.POST)

        if form.is_valid():

            messages.append("Inregistrare cu success")
            context = {"messages": messages}
            form.save()
            send_mail(
                'Confirmare inregistrare',
                ('Cont creat cu succes'),
                'razvanazxc@gmail.com',
                [request.user.email],
                fail_silently=False,
            )
            return render(request, "accounts/register.html", context)

    context = {'form': form}
    return render (request, 'accounts/register.html', context)


def HistoryDetail(request, pk):
    item = Product.objects.get(id=pk)
    item2 = History()
    item2.activation_code = 123456789
    print(request.user)
    has_money = Wallet.objects.get(author=request.user)
    item2.author = MyUser.objects.get(pk=request.user.pk)
    item2.item = Product.objects.get(id=pk)
    item.quantity = item.quantity - 1
    if item.quantity <= 0:
        item.quantity = 0
    item.save()
    has_money.save()
    item2.save()
    if has_money.balance >= item.price:
        has_money.balance = has_money.balance - item.price
        has_money.save()
        return render(request, 'accounts/basket.html', {'item': item, 'wallet': has_money})
    else:
        return render(request, 'accounts/no_founds_error.html')



class Purchased(ListView):
    template_name = "accounts/history.html"
    model = History


class User_Wallet(ListView):
    template_name = "accounts/money_balance.html"
    model = Wallet

