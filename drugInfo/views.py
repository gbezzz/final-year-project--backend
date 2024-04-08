'''from django.shortcuts import render
from django.http import HttpResponse

def drugInfo(request):
    return HttpResponse("General Drug Information Handler")
'''
'''from rest_framework.views import APIView
from rest_framework.response import Response
from pymongo import MongoClient
from rest_framework import generics
from django.db.models import Q
from .models import Drug
from .serializers import DrugInfoSerializer 
from rest_framework import filters

client = MongoClient('mongodb+srv://Josh:kozaYq63yQPeedwG@cluster0.iqe8x2k.mongodb.net/')  # Connect to MongoDB server
db = client['sample_medicines']  # Connect to your MongoDB database
collection = db['OrthodoxDrug']  # Connect to your MongoDB collection
class DrugListAPIView(generics.ListAPIView):
    queryset = Drug.objects.all()
    serializer_class = DrugInfoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'state', ...]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            # Create a Q object to combine queries for each field
            search_fields = [field + '__icontains' for field in self.search_fields]
            q_objects = Q()
            for field in search_fields:
                q_objects |= Q(**{field: search_query})
            queryset = queryset.filter(q_objects)
        return queryset
        '''




'''class DrugSearch(APIView):
    def get(self, request):
        query_params = request.query_params
        query = {}

        # Build query based on query params
        for key, value in query_params.items():
            query[key] = value

        # Connect to MongoDB
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.MONGO_DB_NAME]

        # Search for drugs
        drugs_collection = db['drugs']
        drugs = drugs_collection.find(query)

        # Serialize the data if needed
        # This is just a basic example, you may need to customize this
        results = [{"name": drug["name"], "manufacturer": drug["manufacturer"]} for drug in drugs]

        return Response(results)
        '''