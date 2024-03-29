from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import History
from .serializers import HistorySerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "patient_last_name",
        "patient_first_name",
        "patient_phone_number",
        "patient_email",
        "doctor_name",
    ]
