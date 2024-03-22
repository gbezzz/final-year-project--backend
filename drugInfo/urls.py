from django.urls import path, include
from . import views

urlpatterns = [
    path("",views.general_drug_information,name="general_drug_information"),
]