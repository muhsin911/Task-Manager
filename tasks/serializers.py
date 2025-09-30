from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        if data.get('status') == 'Completed':
            if not data.get('completion_report') or not data.get('worked_hours'):
                raise serializers.ValidationError("Completion report and worked hours are required for completed tasks.")
        return data

class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['completion_report', 'worked_hours']