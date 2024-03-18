from django.shortcuts import render
from django.http import HttpResponse
'''
    path("home/",views.home,name="home"),
    path("drug-recommendation-tool/",views.drug_recommendation_tool,name="drug_recommendation_tool"),
    path("drug-recommendation-history/",views.drug_recommendation_history,name="drug_recommendation_history"),
    path("general-drug-information/",views.general_drug_information,name="general_drug_information"),
'''
def home(request):
    return HttpResponse("Home handler")

def drug_recommendation_tool(request):
    return HttpResponse("Drug Recommendation Tool handler")

def drug_recommendation_history(request):
    return HttpResponse("Drug Recommendation History handler")

def general_drug_information(request):
    return HttpResponse("General Drug Information Handler")