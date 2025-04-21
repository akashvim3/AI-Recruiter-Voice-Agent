from rest_framework import serializers
from .models import Job, JobApplication, JobMatch

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ('posted_by', 'created_at', 'updated_at')

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ('candidate', 'applied_at', 'updated_at')

class JobMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobMatch
        fields = '__all__'
        read_only_fields = ('created_at',)