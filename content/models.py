# content/models.py

from django.db import models
from django.contrib.auth.models import User
import yfinance as yf

class Stock(models.Model):
    company_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.symbol} - {self.name}"

    def save(self, *args, **kwargs):
        # Format price to always display as 00000.00
        self.price = format(self.price, '.2f')
        super().save(*args, **kwargs)

    def get_live_price(self):
        try:
            ticker = yf.Ticker(self.symbol)
            data = ticker.history(period='1d')
            if not data.empty:
                return data['Close'].iloc[0]  # Update to use iloc for position-based access
        except Exception as e:
            print(f"Error fetching live price for {self.symbol}: {str(e)}")
        return None

class Dashboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.stock.symbol}"
