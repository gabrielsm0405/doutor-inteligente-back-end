from rest_framework import serializers
from .models import Results

class ResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Results
        fields = ['key', 'originalImage']