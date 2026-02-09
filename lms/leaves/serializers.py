from rest_framework import serializers
from .models import LeaveRequest

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ['status','user']

    def validate(self,data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("Start date cannot be after end date.")  
        return data