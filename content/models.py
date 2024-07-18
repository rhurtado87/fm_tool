
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

    def get_live_price(self):
        ticker = yf.Ticker(self.symbol)
        data = ticker.history(period='1d')
        return data['Close'][0]  # Assuming you want the closing price for the day

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.stock.symbol}"
