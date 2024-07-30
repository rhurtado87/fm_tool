# pages/views.py
from django.shortcuts import render , redirect
from .forms import ContactForm
from django.core.mail import send_mail
from django.template.loader import render_to_string

def home(request):
    return render(request, 'pages/home.html')

def portfolio(request):
    return render(request, 'pages/portfolio.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

    else:
        form = ContactForm()

    return render(request, 'pages/help.html', {"form": form })

def market(request):
    return render(request, 'content/market.html')

def transactions(request):
    return render(request, 'pages/transactions.html')