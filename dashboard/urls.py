from django.urls import path, include
from . import views

urlpatterns = [
    path("home/",views.home,name="home"),
    path("drug-recommendation-tool/",views.drug_recommendation_tool,name="drug_recommendation_tool"),
    path("drug-recommendation-history/",views.drug_recommendation_history,name="drug_recommendation_history"),
    path("general-drug-information/",views.general_drug_information,name="general_drug_information"),  

]
