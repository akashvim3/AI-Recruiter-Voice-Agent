from rest_framework import serializers
from .models import CandidateProfile, CandidateSkill, CandidateExperience

class CandidateSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSkill
        fields = '__all__'

class CandidateExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateExperience
        fields = '__all__'

class CandidateProfileSerializer(serializers.ModelSerializer):
    skills = CandidateSkillSerializer(many=True, read_only=True)
    experiences = CandidateExperienceSerializer(many=True, read_only=True)

    class Meta:
        model = CandidateProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at') 