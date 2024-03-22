from django.shortcuts import render
from rest_framework import viewsets
from .models import Patient, Diagnose
from .serializers import PatientSerializer, DiagnoseSerializer, ReportSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]


class DiagnoseViewSet(viewsets.ModelViewSet):
    queryset = Diagnose.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Diagnose.objects.all()
        return Diagnose.objects.filter(doctor=self.request.user)

    serializer_class = DiagnoseSerializer
    permission_classes = [IsAuthenticated]

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

    def get_queryset(self):

        if self.request.user.is_superuser:
            return Diagnose.objects.all()
        return Diagnose.objects.filter(doctor=self.request.user)

    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
