from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StockSearchForm
from .models import Stock, Dashboard
import yfinance as yf
import pandas as pd

import random
from django.http import JsonResponse
from .models import Stock

# Function to fetch stock data from Yahoo Finance
def fetch_stock_from_yahoo(company_name):
    try:
        stock = yf.Ticker(company_name)
        data = stock.history(period='1d')
        
        if data.empty:
            return None, f"No stock data found for {company_name}. Please check the symbol and try again."
        
        latest_data = data.iloc[-1]
        
        return {
            'symbol': company_name,
            'name': stock.info['longName'],
            'price': latest_data['Close']
        }, None
    
    except Exception as e:
        error_msg = f"Error fetching data: {str(e)}"
        print(error_msg)
        return None, error_msg

@login_required
def dashboard_view(request):
    dashboard_items = Dashboard.objects.filter(user=request.user)
    stock_symbols = [item.stock.symbol for item in dashboard_items]

    live_prices, errors, historical_data = {}, {}, {}
    for symbol in stock_symbols:
        live_price, error = fetch_stock_from_yahoo(symbol)
        if live_price:
            live_prices[symbol] = live_price['price']
            
             # Fetch historical data (e.g., last 30 days)
            stock = yf.Ticker(symbol)
            history = stock.history(period='1mo')  # Use a valid period
            if not history.empty:
                historical_data[symbol] = {
                    'labels': history.index.strftime('%Y-%m-%d').tolist(),
                    'data': history['Close'].tolist()
                }
            else:
                historical_data[symbol] = {'labels': [], 'data': []}

        else:
            errors[symbol] = error
    
    # Update prices in database
    for item in dashboard_items:
        if item.stock.symbol in live_prices:
            item.stock.price = live_prices[item.stock.symbol]
            item.stock.save()
        else:
            item.stock.price = None
            item.stock.save()
    
    return render(request, 'accounts/dashboard.html', {
        'dashboard_items': dashboard_items,
        'errors': errors,
        'historical_data': historical_data
    })


@login_required
def display_stock(request, stock_id):
    stock = get_object_or_404(Stock, pk=stock_id)
    live_price, error = fetch_stock_from_yahoo(stock.symbol)
    
    if live_price:
        context = {
            'stock': stock,
            'live_price': live_price['price'],
        }
    else:
        context = {
            'stock': stock,
            'live_price': None,
            'error_message': error if error else f"Failed to retrieve live price for {stock.symbol}."
        }
    
    return render(request, 'content/stock_detail.html', context)

@login_required
def search_stock(request):
    form = StockSearchForm()
    stock = None

    if request.method == 'POST':
        form = StockSearchForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            stock_data, error = fetch_stock_from_yahoo(company_name)

            if stock_data:
                stock, created = Stock.objects.get_or_create(
                    symbol=stock_data['symbol'],
                    defaults={'name': stock_data['name'], 'price': stock_data['price']}
                )

                if created or not Dashboard.objects.filter(user=request.user, stock=stock).exists():
                    Dashboard.objects.create(user=request.user, stock=stock)
                    messages.success(request, f"{stock_data['name']} added to your Dashboard.")
                else:
                    messages.info(request, f"{stock_data['name']} is already in your Dashboard.")

            else:
                messages.error(request, error if error else f"No stock data found for {company_name}.")

    return render(request, 'content/search_stock.html', {'form': form, 'stock': stock})

@login_required
def add_to_dashboard(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)

    if request.method == 'POST':
        dashboard_item, created = Dashboard.objects.get_or_create(user=request.user, stock=stock)
        if created:
            messages.success(request, f"{stock.name} added to your Dashboard.")
        else:
            messages.info(request, f"{stock.name} is already in your Dashboard.")

    return redirect('dashboard')

@login_required
def remove_from_dashboard(request, stock_id):
    dashboard_item = get_object_or_404(Dashboard, user=request.user, stock__id=stock_id)

    if request.method == 'POST':
        stock_name = dashboard_item.stock.name
        dashboard_item.delete()
        messages.success(request, f"{stock_name} removed from your dashboard.")

    return redirect('dashboard')

@login_required
def fetch_stock_data(request, symbol, period):
    try:
        # Validate period
        valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        if period not in valid_periods:
            return JsonResponse({'error': 'Invalid period'}, status=400)
        
        stock = yf.Ticker(symbol)
        history = stock.history(period=period)
        
        if history.empty:
            return JsonResponse({'error': 'No data found'}, status=404)

        # Prepare data for Charts.js
        labels = history.index.strftime('%Y-%m-%d').tolist()
        open_prices = history['Open'].tolist()
        close_prices = history['Close'].tolist()

        datasets = [
            {
                'label': 'Opening Price',
                'data': [{'x': labels[i], 'y': open_prices[i]} for i in range(len(open_prices))],
                'borderColor': 'rgba(75, 192, 192, 1)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'fill': false,
                'tension': 0.1
            },
            {
                'label': 'Closing Price',
                'data': [{'x': labels[i], 'y': close_prices[i]} for i in range(len(close_prices))],
                'borderColor': 'rgba(153, 102, 255, 1)',
                'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                'fill': false,
                'tension': 0.1
            }
        ]

        return JsonResponse({'labels': labels, 'datasets': datasets})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def getRandomColor():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))