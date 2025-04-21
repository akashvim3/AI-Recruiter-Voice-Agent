from django.db import models
from django.conf import settings
from django.utils import timezone

class Interview(models.Model):
    INTERVIEW_STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    INTERVIEW_TYPE_CHOICES = [
        ('PHONE', 'Phone Interview'),
        ('VIDEO', 'Video Interview'),
        ('ONSITE', 'On-site Interview'),
        ('TECHNICAL', 'Technical Assessment'),
    ]

    candidate = models.ForeignKey(
        'candidates.Candidate',
        on_delete=models.CASCADE,
        related_name='interviews'
    )
    interviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interviews_conducted'
    )
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='interviews'
    )
    scheduled_date = models.DateTimeField()
    duration = models.IntegerField(help_text='Duration in minutes')
    status = models.CharField(
        max_length=20,
        choices=INTERVIEW_STATUS_CHOICES,
        default='SCHEDULED'
    )
    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPE_CHOICES
    )
    meeting_link = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    rating = models.IntegerField(
        null=True,
        blank=True,
        help_text='Rating from 1 to 5'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date']
        indexes = [
            models.Index(fields=['scheduled_date']),
            models.Index(fields=['status']),
            models.Index(fields=['interview_type']),
        ]

    def __str__(self):
        return f"{self.candidate} - {self.job} - {self.scheduled_date}"

class InterviewQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('TECHNICAL', 'Technical'),
        ('BEHAVIORAL', 'Behavioral'),
        ('PROBLEM_SOLVING', 'Problem Solving'),
        ('SYSTEM_DESIGN', 'System Design'),
    ]

    interview = models.ForeignKey(
        Interview,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES
    )
    expected_answer = models.TextField(blank=True)
    candidate_answer = models.TextField(blank=True)
    score = models.IntegerField(
        null=True,
        blank=True,
        help_text='Score from 1 to 10'
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['question_type']
        indexes = [
            models.Index(fields=['question_type']),
        ]

    def __str__(self):
        return f"{self.interview} - {self.question_type}"

class InterviewFeedback(models.Model):
    interview = models.OneToOneField(
        Interview,
        on_delete=models.CASCADE,
        related_name='interview_feedback'
    )
    strengths = models.TextField()
    weaknesses = models.TextField()
    overall_rating = models.IntegerField(
        help_text='Overall rating from 1 to 5'
    )
    technical_skills_rating = models.IntegerField(
        help_text='Technical skills rating from 1 to 5'
    )
    communication_skills_rating = models.IntegerField(
        help_text='Communication skills rating from 1 to 5'
    )
    problem_solving_rating = models.IntegerField(
        help_text='Problem solving rating from 1 to 5'
    )
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback for {self.interview}" 