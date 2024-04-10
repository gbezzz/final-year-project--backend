from django.shortcuts import render
from rest_framework import viewsets, filters, serializers
from .models import Patient, Diagnose
from .serializers import (
    PatientSerializer,
    DiagnoseSerializer,
    ReportSerializer,
    DrugSerializer,
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
from drugInfo.models import OrthodoxDrug, TraditionalDrug


# Create your views here.


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
    ]


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
        orthodox_drug_ids = self.request.data.get("orthodox_drug_ids", "").split(",")
        traditional_drug_ids = self.request.data.get("traditional_drug_ids", "").split(
            ","
        )

        # Validate that the provided drug IDs exist in the database
        if not all(
            OrthodoxDrug.objects.filter(id=id).exists() for id in orthodox_drug_ids
        ):
            raise ValidationError("One or more orthodox drug IDs do not exist.")
        if not all(
            TraditionalDrug.objects.filter(id=id).exists()
            for id in traditional_drug_ids
        ):
            raise ValidationError("One or more traditional drug IDs do not exist.")

        serializer.save(
            doctor_name=user.get_full_name(),
            doctor_phone=user.phone_number,
            doctor_email=user.email,
            orthodox_drug_ids=",".join(orthodox_drug_ids),
            traditional_drug_ids=",".join(traditional_drug_ids),
        )

    @action(detail=True, methods=["post"])
    def select_drugs(self, request, pk=None):
        selected_orthodox_drug_ids = request.data.get("selected_orthodox_drug_ids", [])
        selected_traditional_drug_ids = request.data.get(
            "selected_traditional_drug_ids", []
        )

        # Validate that the provided drug IDs exist in the database
        if not all(
            OrthodoxDrug.objects.filter(id=id).exists()
            for id in selected_orthodox_drug_ids
        ):
            raise ValidationError("One or more orthodox drug IDs do not exist.")
        if not all(
            TraditionalDrug.objects.filter(id=id).exists()
            for id in selected_traditional_drug_ids
        ):
            raise ValidationError("One or more traditional drug IDs do not exist.")

        diagnose = self.get_object()
        diagnose.orthodox_drug_ids = ",".join(map(str, selected_orthodox_drug_ids))
        diagnose.traditional_drug_ids = ",".join(
            map(str, selected_traditional_drug_ids)
        )
        diagnose.save()

        return Response(self.get_serializer(diagnose).data)


# Logic for the Drug Recommendation Tool
class RecommendDrugsView(APIView):
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DrugSerializer

    def get(self, request):
        # Retrieve the diagnosis and patient ID from the request's query parameters.
        diagnosis = request.query_params.get("diagnosis", None)
        patient_id = request.query_params.get("patient_id", None)

        # Check if both diagnosis and patient ID are provided.
        if diagnosis is not None and patient_id is not None:
            # Try to retrieve the patient from the database. If the patient does not exist, raise a NotFound exception.
            try:
                patient = Patient.objects.get(id=patient_id)
            except Patient.DoesNotExist:
                raise NotFound(detail="Patient does not exist")

            # Check if the diagnosis exists in the database. If not, raise a NotFound exception.
            diagnose = Diagnose.objects.filter(name=diagnosis).first()
            if not diagnose:
                raise NotFound(detail="Diagnosis does not exist")

            # Retrieve the patient's age, sex, and weight.
            age = patient.age
            sex = patient.sex
            weight = patient.weight

            # Retrieve the drugs associated with the diagnosis.
            orthodox_drug_ids = list(map(int, diagnose.orthodox_drug_ids.split(",")))
            traditional_drug_ids = list(
                map(int, diagnose.traditional_drug_ids.split(","))
            )
            orthodox_drugs = OrthodoxDrug.objects.filter(id__in=orthodox_drug_ids)
            traditional_drugs = TraditionalDrug.objects.filter(
                id__in=traditional_drug_ids
            )

            # Filter the drugs based on the patient's age, sex, and weight.
            orthodox_drugs = self.filter_drugs(orthodox_drugs, age, sex, weight)
            traditional_drugs = self.filter_drugs(traditional_drugs, age, sex, weight)

            # Return a response containing the recommended orthodox and traditional drugs. The data is serialized using the OrthodoxDrugSerializer and TraditionalDrugSerializer.
            return Response(
                DrugSerializer(
                    {
                        "orthodox_drug": orthodox_drugs,
                        "traditional_drug": traditional_drugs,
                    }
                ).data
            )

        else:
            # If either the diagnosis or patient ID is not provided, return an error response.
            return Response(
                {"error": "No diagnosis or patient ID provided"}, status=400
            )

    # Define a method for filtering drugs based on a patient's age, sex, and weight.
    def filter_drugs(self, drugs, age, sex, weight):
        filtered_drugs = []
        for drug in drugs:
            # Extract the age range, sex, and weight range from the drug information. You'll need to replace these lines with the actual code to extract this information from your drug models.
            drug_age_range = ...  # Extract age range from drug information
            drug_sex = ...  # Extract sex from drug information
            drug_weight_range = ...  # Extract weight range from drug information

            # Check if the patient's age, sex, and weight fall within the drug's parameters. If they do, add the drug to the list of filtered drugs.
            if (
                age in drug_age_range
                and sex == drug_sex
                and weight in drug_weight_range
            ):
                filtered_drugs.append(drug)

        # Return the list of filtered drugs.
        return filtered_drugs


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Diagnose.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Diagnose.objects.all()
        return Diagnose.objects.filter(doctor=self.request.user)

    @action(detail=True, methods=["post"])
    def add_drugs(self, request, pk=None):
        orthodox_drug_ids = request.data.get("orthodox_drug_ids", "").split(",")
        traditional_drug_ids = request.data.get("traditional_drug_ids", "").split(",")

        # Validate that the provided drug IDs exist in the database
        if not all(
            OrthodoxDrug.objects.filter(id=id).exists() for id in orthodox_drug_ids
        ):
            raise ValidationError("One or more orthodox drug IDs do not exist.")
        if not all(
            TraditionalDrug.objects.filter(id=id).exists()
            for id in traditional_drug_ids
        ):
            raise ValidationError("One or more traditional drug IDs do not exist.")

        report = self.get_object()
        report.orthodox_drug_ids = ",".join(orthodox_drug_ids)
        report.traditional_drug_ids = ",".join(traditional_drug_ids)

        # Get the names of the selected orthodox and traditional drugs
        orthodox_drugs = OrthodoxDrug.objects.filter(id__in=orthodox_drug_ids)
        traditional_drugs = TraditionalDrug.objects.filter(id__in=traditional_drug_ids)
        selected_drugs = [drug.name for drug in orthodox_drugs] + [
            drug.name for drug in traditional_drugs
        ]
        report.selected_drug = ", ".join(selected_drugs)
        report.save()

        return Response(self.get_serializer(report).data)

    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
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
