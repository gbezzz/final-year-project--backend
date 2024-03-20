from django.shortcuts import render
from rest_framework import viewsets
from .models import Patient, Diagnose
from .serializers import PatientSerializer, DiagnoseSerializer, ReportSerializer

# Create your views here.


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DiagnoseViewSet(viewsets.ModelViewSet):
    queryset = Diagnose.objects.all()
    serializer_class = DiagnoseSerializer


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Diagnose.objects.all()
    serializer_class = ReportSerializer
