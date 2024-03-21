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

    def perform_create(self, serializer):
        # Set the doctor's details from the request user
        user = self.request.user
        serializer.save(
            doctor_name=user.get_full_name(),
            doctor_phone=user.phone_number,
            doctor_email=user.email,
        )


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Diagnose.objects.all()
    serializer_class = ReportSerializer
