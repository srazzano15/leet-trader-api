# models.py
from django.db import models
from django.contrib.auth.models import User  # Importing the default User model

class Transaction(models.Model):
    BUY = 'buy'
    SELL = 'sell'
    TRANSACTION_TYPES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    ticker = models.CharField(max_length=10)  # Stock or crypto symbol (e.g., BTCUSD, AAPL)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)  # Buy or sell
    quantity = models.DecimalField(max_digits=10, decimal_places=4)  # Number of units bought/sold
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Price at which the transaction occurred
    total_value = models.DecimalField(max_digits=15, decimal_places=2)  # Total value of the transaction
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the transaction

    def __str__(self) -> str:
        return f'{self.transaction_type.capitalize()} {self.quantity} {self.ticker} at {self.price_per_unit} each'


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portfolio')
    total_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Total money invested
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Current total value of all holdings
    created_at = models.DateTimeField(auto_now_add=True)  # When the portfolio was created
    updated_at = models.DateTimeField(auto_now=True)  # When the portfolio was last updated

    def __str__(self) -> str:
        return f"{self.user.username}'s Portfolio"
