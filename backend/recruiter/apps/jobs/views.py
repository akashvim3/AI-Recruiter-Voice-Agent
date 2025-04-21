from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job, JobApplication, JobMatch
from .serializers import JobSerializer, JobApplicationSerializer, JobMatchSerializer
from django.shortcuts import get_object_or_404

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        job = self.get_object()
        serializer = JobApplicationSerializer(data={
            'job': job.id,
            'candidate': request.user.id,
            'cover_letter': request.data.get('cover_letter'),
            'resume': request.data.get('resume')
        })
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return JobApplication.objects.all()
        return JobApplication.objects.filter(candidate=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            return Response(JobApplicationSerializer(application).data)
        return Response(
            {'error': 'Invalid status'},
            status=status.HTTP_400_BAD_REQUEST
        )

class JobMatchViewSet(viewsets.ModelViewSet):
    queryset = JobMatch.objects.all()
    serializer_class = JobMatchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return JobMatch.objects.all()
        return JobMatch.objects.filter(candidate=self.request.user)

    @action(detail=False, methods=['get'])
    def recommended_jobs(self, request):
        matches = JobMatch.objects.filter(
            candidate=request.user
        ).order_by('-match_score')[:10]
        serializer = self.get_serializer(matches, many=True)
        return Response(serializer.data) 