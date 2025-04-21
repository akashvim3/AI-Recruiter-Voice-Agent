from rest_framework import serializers
from .models import Interview, InterviewQuestion, InterviewFeedback
from django.utils import timezone

class InterviewQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewQuestion
        fields = [
            'id', 'question_text', 'question_type', 'expected_answer',
            'candidate_answer', 'score', 'notes'
        ]

class InterviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewFeedback
        fields = [
            'id', 'strengths', 'weaknesses', 'overall_rating',
            'technical_skills_rating', 'communication_skills_rating',
            'problem_solving_rating', 'recommendation', 'created_at',
            'updated_at'
        ]

class InterviewSerializer(serializers.ModelSerializer):
    questions = InterviewQuestionSerializer(many=True, read_only=True)
    feedback = InterviewFeedbackSerializer(read_only=True)
    candidate_name = serializers.CharField(source='candidate.user.get_full_name', read_only=True)
    interviewer_name = serializers.CharField(source='interviewer.get_full_name', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Interview
        fields = [
            'id', 'candidate', 'candidate_name', 'interviewer', 'interviewer_name',
            'job', 'job_title', 'scheduled_date', 'duration', 'status',
            'interview_type', 'meeting_link', 'notes', 'feedback', 'rating',
            'questions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_scheduled_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Interview cannot be scheduled in the past")
        return value

    def validate_duration(self, value):
        if value < 15 or value > 240:
            raise serializers.ValidationError("Duration must be between 15 and 240 minutes")
        return value

class InterviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = [
            'candidate', 'interviewer', 'job', 'scheduled_date',
            'duration', 'interview_type', 'meeting_link', 'notes'
        ]

    def validate(self, data):
        # Check if the candidate has already been interviewed for this job
        existing_interview = Interview.objects.filter(
            candidate=data['candidate'],
            job=data['job'],
            status__in=['SCHEDULED', 'IN_PROGRESS']
        ).exists()
        
        if existing_interview:
            raise serializers.ValidationError(
                "This candidate already has a scheduled or in-progress interview for this job"
            )
        
        return data

class InterviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = [
            'status', 'notes', 'feedback', 'rating', 'meeting_link'
        ]

    def validate_status(self, value):
        if value == 'COMPLETED' and not self.instance.feedback:
            raise serializers.ValidationError(
                "Feedback is required before marking the interview as completed"
            )
        return value 