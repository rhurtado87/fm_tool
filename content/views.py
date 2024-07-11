import yfinance as yf
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Stock, Wishlist
from .forms import StockSearchForm
from django.contrib.auth.decorators import login_required


# Function to fetch stock data from Yahoo Finance
def fetch_stock_from_yahoo(company_name):
    try:
        # Use yfinance to fetch stock data
        stock = yf.Ticker(company_name)
        data = stock.history(period='1d')  # Fetch daily historical data
        
        if data.empty:
            return None, f"No stock data found for {company_name}. Please check the symbol and try again."
        
        latest_data = data.iloc[-1]  # Get the latest data point
        
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
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'content/wishlist.html', {'wishlist_items': wishlist_items})

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

                if created or not Wishlist.objects.filter(user=request.user, stock=stock).exists():
                    Wishlist.objects.create(user=request.user, stock=stock)
                    messages.success(request, f"{stock_data['name']} added to your wishlist.")
                else:
                    messages.info(request, f"{stock_data['name']} is already in your wishlist.")

            else:
                messages.error(request, error if error else f"No stock data found for {company_name}.")
    
    return render(request, 'content/search_stock.html', {'form': form, 'stock': stock})


def add_to_wishlist(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    
    if request.method == 'POST':
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, stock=stock)
        if created:
            messages.success(request, f"{stock.name} added to your Watchlist.")
        else:
            messages.info(request, f"{stock.name} is already in your Watchlist.")
    
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, stock_id):
    wishlist_item = get_object_or_404(Wishlist, user=request.user, stock__id=stock_id)
    
    if request.method == 'POST':
        stock_name = wishlist_item.stock.name
        wishlist_item.delete()
        messages.success(request, f"{stock_name} removed from your wishlist.")
    
    return redirect('wishlist')