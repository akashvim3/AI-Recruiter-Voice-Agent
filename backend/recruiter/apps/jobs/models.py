from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)  # Full-time, Part-time, Contract
    experience_level = models.CharField(max_length=50)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('REVIEWING', 'Reviewing'),
        ('SHORTLISTED', 'Shortlisted'),
        ('REJECTED', 'Rejected'),
        ('HIRED', 'Hired'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate.email} - {self.job.title}"

class JobMatch(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    match_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.email} - {self.job.title} ({self.match_score}%)"