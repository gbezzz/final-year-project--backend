# drug_info_app/serializers.py
from rest_framework import serializers
from .models import OrthodoxDrug, TraditionalDrug

class OrthodoxDrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrthodoxDrug
        fields = '__all__'

class TraditionalDrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraditionalDrug
        fields = '__all__'
