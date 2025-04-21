from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from .models import Interview, InterviewQuestion, InterviewFeedback
from .serializers import (
    InterviewSerializer, InterviewCreateSerializer,
    InterviewUpdateSerializer, InterviewQuestionSerializer,
    InterviewFeedbackSerializer
)
from .permissions import IsInterviewerOrAdmin
from .tasks import send_interview_reminder, send_interview_feedback

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsInterviewerOrAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return InterviewCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return InterviewUpdateSerializer
        return InterviewSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Interview.objects.all()
        
        # For interviewers, show their interviews
        if hasattr(user, 'interviewer_profile'):
            return Interview.objects.filter(
                Q(interviewer=user) | Q(candidate__user=user)
            )
        
        # For candidates, show only their interviews
        return Interview.objects.filter(candidate__user=user)

    @action(detail=True, methods=['post'])
    def add_question(self, request, pk=None):
        interview = self.get_object()
        serializer = InterviewQuestionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(interview=interview)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def submit_feedback(self, request, pk=None):
        interview = self.get_object()
        serializer = InterviewFeedbackSerializer(data=request.data)
        
        if serializer.is_valid():
            feedback = serializer.save(interview=interview)
            interview.feedback = feedback.recommendation
            interview.status = 'COMPLETED'
            interview.save()
            
            # Send feedback notification
            send_interview_feedback.delay(interview.id)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def start_interview(self, request, pk=None):
        interview = self.get_object()
        if interview.status != 'SCHEDULED':
            return Response(
                {"error": "Interview is not in scheduled state"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        interview.status = 'IN_PROGRESS'
        interview.save()
        return Response({"status": "Interview started"})

    @action(detail=True, methods=['post'])
    def cancel_interview(self, request, pk=None):
        interview = self.get_object()
        if interview.status not in ['SCHEDULED', 'IN_PROGRESS']:
            return Response(
                {"error": "Interview cannot be cancelled in its current state"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        interview.status = 'CANCELLED'
        interview.save()
        return Response({"status": "Interview cancelled"})

    def perform_create(self, serializer):
        interview = serializer.save()
        # Schedule reminder emails
        send_interview_reminder.apply_async(
            args=[interview.id],
            eta=interview.scheduled_date - timezone.timedelta(hours=24)
        )

class InterviewQuestionViewSet(viewsets.ModelViewSet):
    queryset = InterviewQuestion.objects.all()
    serializer_class = InterviewQuestionSerializer
    permission_classes = [permissions.IsAuthenticated, IsInterviewerOrAdmin]

    def get_queryset(self):
        return InterviewQuestion.objects.filter(
            interview__interviewer=self.request.user
        )

class InterviewFeedbackViewSet(viewsets.ModelViewSet):
    queryset = InterviewFeedback.objects.all()
    serializer_class = InterviewFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsInterviewerOrAdmin]

    def get_queryset(self):
        return InterviewFeedback.objects.filter(
            interview__interviewer=self.request.user
        ) 