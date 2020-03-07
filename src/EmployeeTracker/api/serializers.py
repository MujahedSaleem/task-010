from rest_framework import serializers
from ..models import Attendants, Vacation, Leave


class AttendantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendants
        fields = '__all__'


class VacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = '__all__'


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'
