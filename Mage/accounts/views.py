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
            tooken = MyUser.objects.get(email=form.cleaned_data['email'])
            send_mail(
                'Confirmare inregistrare',
                ('Cont creat cu succes \n Tokenul este: '+str(tooken.activation_token)+
                 "\nlink activare: "+"http://127.0.0.1:8000/emailconfirm/"+str(tooken.activation_token)),
                'razvanazxc@gmail.com',
                [form.cleaned_data['email']],
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


def email_confirm(request, activation_token):
    user = MyUser.objects.get(activation_token=activation_token)
    if user:
        user.is_active = True
        user.activation_token = 'f4a93f89-6b6e-4b2d-aa54-19eb7a268cef'
        user.save()
        context = {'user': user}
        return render(request, "accounts/email_activated.html", context)
    else:
        return render(request, "accounts/home_list.html")

