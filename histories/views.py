from django.shortcuts import render
from rest_framework import viewsets
from .models import History
from .serializers import HistorySerializer

# Create your views here.


class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
