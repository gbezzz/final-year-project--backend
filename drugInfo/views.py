from django.shortcuts import render
from django.http import HttpResponse

def general_drug_information(request):
    return HttpResponse("General Drug Information Handler")

