from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    current_position = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    skills = models.TextField()
    education = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s Profile"

class CandidateSkill(models.Model):
    SKILL_LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('EXPERT', 'Expert'),
    ]

    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES)
    years_of_experience = models.IntegerField()

    def __str__(self):
        return f"{self.candidate.user.email} - {self.skill_name}"

class CandidateExperience(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    current_job = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        return f"{self.candidate.user.email} - {self.position} at {self.company_name}" 