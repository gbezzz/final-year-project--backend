# from django.shortcuts import render, get_object_or_404
# from rest_framework import viewsets, filters, serializers
# from .models import Patient, Diagnosis
# from .serializers import (
#     PatientSerializer,
#     DiagnosisSerializer,
#     ReportSerializer,
#     TradDrugSerializer,
# )
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.decorators import (
#     api_view,
#     authentication_classes,
#     permission_classes,
#     action,
# )
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.exceptions import NotFound, ValidationError
# from .models import TradDrug


# # class RecommendationsView(APIView):
# #     permission_classes = [IsAuthenticated]  # Add your authentication class as needed

# #     def get(self, request):
# #         diagnosis_name = request.query_params.get("diagnosis", None)

# #         if diagnosis_name is not None:
# #             # Find the diagnosis
# #             diagnosis = get_object_or_404(Diagnosis, name=diagnosis_name)

# #             # Filter drugs that have this diagnosis in their indication
# #             drugs = Drug.objects.filter(drug_indication__icontains=diagnosis_name)

# #             # Serialize the drug data
# #             serializer = DrugSerializer(drugs, many=True)
# #             return Response(serializer.data)
# #         else:
# #             return Response({"error": "No diagnosis provided"}, status=400)


# class PatientViewSet(viewsets.ModelViewSet):
#     queryset = Patient.objects.all()
#     # authentication_classes = [JWTAuthentication]
#     serializer_class = PatientSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter]
#     search_fields = [
#         "first_name",
#         "last_name",
#         "email",
#         "phone_number",
#     ]


# class DiagnosisViewSet(viewsets.ModelViewSet):
#     queryset = Diagnosis.objects.all()
#     # authentication_classes = [JWTAuthentication]
#     serializer_class = DiagnosisSerializer
#     permission_classes = [IsAuthenticated]

#     # def get_queryset(self):
#     #     if self.request.user.is_superuser:
#     #         return Diagnosis.objects.all()
#     #     return Diagnosis.objects.filter(doctor=self.request.user)

#     # def perform_create(self, serializer):
#     #     user = self.request.user
#     #     traditional_drug_ids = (
#     #         self.request.data.get("traditional_drug_ids", "").split(",")
#     #         if self.request.data.get("traditional_drug_ids")
#     #         else []
#     #     )

#     #     if not all(
#     #         TradDrug.objects.filter(traditional_drug_ids=id).exists()
#     #         for id in traditional_drug_ids
#     #     ):
#     #         raise ValidationError("One or more traditional drug IDs do not exist.")

#     #     serializer.save(
#     #         doctor_name=user.get_full_name(),
#     #         doctor_phone=user.phone_number,
#     #         doctor_email=user.email,
#     #         traditional_drug_ids=",".join(traditional_drug_ids),
#     #     )

#     @api_view(["GET"])
#     def select_drugs(self, request, pk=None):
#         # diagnosis = self.get_object()
#         recommend_drugs_view = RecommendTradDrugsView()
#         disease_indications = request.query_params.get("disease_indications", None)
#         response = recommend_drugs_view.get(disease_indications=disease_indications)

#         return Response(response.data)

#     # @action(detail=True, methods=["post"])
#     # def save_selected_drugs(self, request, pk=None):
#     #     selected_drugs = request.data.get("selected_drugs", "").split(",")
#     #     diagnosis = self.get_object()
#     #     recommend_trad_drugs_view = RecommendTradDrugView()
#     #     response = recommend_trad_drugs_view.get(
#     #         request._request, disease_indications=diagnosis.name
#     #     )
#     #     recommended_drugs = response.data

#     #     for drug in selected_drugs:
#     #         if drug not in [drug["product_name"] for drug in recommended_drugs]:
#     #             raise ValidationError(
#     #                 f"{drug} is not in the list of recommended drugs."
#     #             )

#     #     diagnosis.selected_drug = ", ".join(selected_drugs)
#     #     diagnosis.save()

#     #     return Response(self.get_serializer(diagnosis).data)


# # Logic for the Drug Recommendation Tool
# class RecommendTradDrugsView(APIView):
#     # authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = TradDrugSerializer

#     def get(self, disease_indications, *args, **kwargs):
#         # disease_indications = request.query_params.get("disease_indications", None)
#         if disease_indications is None:
#             return Response(
#                 {"error": "disease_indications parameter is required"}, status=400
#             )

#         filtered_drugs = TradDrug.objects.filter(
#             disease_indications=disease_indications
#         )
#         if not filtered_drugs.exists():
#             raise ValidationError("No drugs found with the given disease indications")

#         serializer = TradDrugSerializer(filtered_drugs, many=True)
#         return Response(serializer.data)


# class ReportViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Diagnosis.objects.all()
#     # authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = ReportSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = [
#         "patient__last_name",
#         "patient__first_name",
#         "patient__phone_number",
#         "patient__email",
#         "patient__address",
#         "diagnosis_made",
#         "doctor_name",
#     ]

#     def get_queryset(self):
#         if self.request.user.is_superuser:
#             return Diagnosis.objects.all()
#         return Diagnosis.objects.filter(doctor=self.request.user)

#     @action(detail=True, methods=["post"])
#     def add_drugs(self, request, pk=None):
#         # orthodox_drug_ids = request.data.get("orthodox_drug_ids", "").split(",")
#         traditional_drug_ids = request.data.get("traditional_drug_ids", "").split(",")

#         # Validate that the provided drug IDs exist in the database
#         # if not all(
#         #      OrthodoxDrug.objects.filter(id=id).exists() for id in orthodox_drug_ids
#         # ):
#         #     raise ValidationError("One or more orthodox drug IDs do not exist.")
#         if not all(
#             TraditionalDrug.objects.filter(id=id).exists()
#             for id in traditional_drug_ids
#         ):
#             raise ValidationError("One or more traditional drug IDs do not exist.")

#         report = self.get_object()
#         # report.orthodox_drug_ids = ",".join(orthodox_drug_ids)
#         report.traditional_drug_ids = ",".join(traditional_drug_ids)

#         # Get the names of the selected orthodox and traditional drugs
#         # orthodox_drugs = OrthodoxDrug.objects.filter(id__in=orthodox_drug_ids)
#         trad_drugs = TradDrug.objects.filter(id__in=traditional_drug_ids)
#         selected_drugs = """[drug.product_name for drug in trad_drugs] ="""
#         [drug.product_name for drug in trad_drugs]
#         report.selected_drug = ", ".join(selected_drugs)
#         report.save()

#         return Response(self.get_serializer(report).data)
