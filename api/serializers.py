from rest_framework import serializers
from .models import DataClass


class DataSerializer(serializers.ModelSerializer):
	class Meta:
		model = DataClass
		fields = ['pk', 'rep_dt', 'delta']
