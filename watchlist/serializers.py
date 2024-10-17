from rest_framework import serializers
from .models import Watchlist

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ['id', 'user', 'assets', 'name', 'created_at']
        read_only_fields = ['user', 'created_at']

    assets = serializers.JSONField(required=False)