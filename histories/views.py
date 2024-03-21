from django.shortcuts import render
from rest_framework import viewsets
from .models import History
from .serializers import HistorySerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]
