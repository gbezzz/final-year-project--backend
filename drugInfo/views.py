"""from django.shortcuts import render
from django.http import HttpResponse

def drugInfo(request):
    return HttpResponse("General Drug Information Handler")
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from pymongo import MongoClient
from rest_framework import viewsets
from django.db.models import Q
from .models import OrthodoxDrug, TraditionalDrug
from .serializers import OrthodoxDrugSerializer, TraditionalDrugSerializer
from rest_framework import filters


def get_queryset(self):
    queryset = super().get_queryset()
    search_query = self.request.query_params.get("search", None)
    if search_query:
        # Create a Q object to combine queries for each field
        search_fields = [field + "__icontains" for field in self.search_fields]
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{field: search_query})
        queryset = queryset.filter(q_objects)
    return queryset


class OrthodoxDrugViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrthodoxDrug.objects.all()
    serializer_class = OrthodoxDrugSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class TraditionalDrugViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TraditionalDrug.objects.all()
    serializer_class = TraditionalDrugSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "Product_Name"
    ]
