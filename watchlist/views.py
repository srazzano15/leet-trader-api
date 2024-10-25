from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Watchlist
from .serializers import WatchlistSerializer


@api_view(['GET', 'POST'])
def watchlist_list(request):
    if request.method == 'GET':
        watchlists = Watchlist.objects.filter(user=request.user)
        serializer = WatchlistSerializer(watchlists, many=True)
        return Response(serializer.data)

    if request.method == 'POST':

        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            watchlist = serializer.save(user=request.user)
            return Response(WatchlistSerializer(watchlist).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def watchlist_detail(request, pk):
    try:
        watchlist = Watchlist.objects.get(pk=pk, user=request.user)
    except Watchlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WatchlistSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PATCH'])
def add_assets_to_watchlist(request, pk):
    try:
        watchlist = Watchlist.objects.get(pk=pk, user=request.user)
    except Watchlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Get existing assets and append new ones
    new_assets = request.data.get('assets', [])
    if not isinstance(new_assets, list):
        return Response({"error": "Assets should be a list"}, status=status.HTTP_400_BAD_REQUEST)

    watchlist.assets.extend(new_assets)
    watchlist.save()

    return Response(WatchlistSerializer(watchlist).data, status=status.HTTP_200_OK)