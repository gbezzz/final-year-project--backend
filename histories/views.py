from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import History
from .serializers import HistorySerializer
from rest_framework.permissions import IsAuthenticated
from djongo import models
# Create your views here.


class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "patient__last_name",
        "patient__first_name",
        "patient__phone_number",
        "patient__email",
        "doctor_name",
    ]
