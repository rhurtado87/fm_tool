# pages/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def portfolio(request):
    return render(request, 'pages/portfolio.html')

def help_support(request):
    return render(request, 'pages/help.html')

def market(request):
    return render(request, 'content/market.html')

def transactions(request):
    return render(request, 'pages/transactions.html')