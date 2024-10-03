from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stocks = models.ManyToManyField(Stock, through='Transaction')

class Transaction(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=10)  # 'buy' or 'sell'
    amount = models.DecimalField(max_digits=10, decimal_places=2)