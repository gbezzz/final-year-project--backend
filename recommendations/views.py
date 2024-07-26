from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters, serializers, status
from .models import Patient, Diagnosis, Report
from .serializers import (
    PatientSerializer,
    DiagnosisSerializer,
    ReportSerializer,
    TraditionalDrugSerializer,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    action,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from .models import TraditionalDrug
from django.db.models import Q
from django.http import JsonResponse


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
    ]


class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "diagnosis_made",
    ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Diagnosis.objects.all()
        return Diagnosis.objects.filter(doctor=self.request.user)

    def perform_create(self, serializer):
        # Set the doctor's details from the request user
        user = self.request.user
        serializer.save(
            doctor_name=user.get_full_name(),
            doctor_phone=user.phone_number,
            doctor_email=user.email,
        )

    @api_view(["GET"])
    def select_drugs(self, request, pk):
        recommend_drugs_view = TradDrugAPIView()
        disease_indications = int(pk)
        response = recommend_drugs_view.get(id=disease_indications)

        return Response(response.data)


class TradDrugAPIView(APIView):
    def get_object(self, pk):
        try:
            return TraditionalDrug.objects.filter(disease_indications__icontains=pk) if not pk.isdigit() else TraditionalDrug.objects.filter(id__icontains=int(pk))
        except TraditionalDrug.DoesNotExist:
            raise NotFound(detail="Traditional drug not found")

    def get(self, request, pk, *args, **kwargs):
        trad_drugs = self.get_object(pk)
        serializer = TraditionalDrugSerializer(trad_drugs, many=True)
        return Response(serializer.data)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "patient__last_name",
        "patient__first_name",
        "patient__phone_number",
        "patient__email",
        "patient__address",
        "diagnosis_made",
        "doctor_name",
    ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Report.objects.all()
        return Report.objects.filter(doctor=self.request.user)


# class ReportViewSet(viewsets.ModelViewSet):
#     queryset = Report.objects.all()
#     serializer_class = ReportSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         reports_data = request.data.get('diagnoses', [])
#         created_reports = []

#         for data in reports_data:
#             diagnosis_queryset = Diagnosis.objects.filter(diagnosis_made=data['diagnosis'])
#             if not diagnosis_queryset.exists():
#                 # Handle case where the diagnosis does not exist
#                 continue

#             diagnosis = diagnosis_queryset.first()

#             report_data = {
#                 'patient_id': request.data.get('patient_id'),
#                 'doctor_id': request.data.get('doctor_id'),
#                 'diagnosis_id': diagnosis.id,
#                 'selected_orthodox_drug': data.get('selected_orthodox_drug'),
#                 'selected_traditional_drug': data.get('selected_traditional_drug'),
#             }

#             serializer = self.get_serializer(data=report_data)
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             created_reports.append(serializer.data)

#         return Response(created_reports, status=status.HTTP_201_CREATED)