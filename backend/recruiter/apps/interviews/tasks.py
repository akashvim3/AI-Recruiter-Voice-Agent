from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Interview

@shared_task
def send_interview_reminder(interview_id):
    """
    Send reminder emails to both interviewer and candidate before the interview.
    """
    try:
        interview = Interview.objects.get(id=interview_id)
        
        # Prepare email context
        context = {
            'interview': interview,
            'candidate_name': interview.candidate.user.get_full_name(),
            'interviewer_name': interview.interviewer.get_full_name(),
            'job_title': interview.job.title,
            'scheduled_date': interview.scheduled_date,
            'duration': interview.duration,
            'interview_type': interview.get_interview_type_display(),
            'meeting_link': interview.meeting_link,
        }

        # Send email to candidate
        candidate_subject = f"Reminder: Upcoming Interview for {interview.job.title}"
        candidate_message = render_to_string(
            'emails/interview_reminder_candidate.html',
            context
        )
        send_mail(
            candidate_subject,
            candidate_message,
            'noreply@recruiter.com',
            [interview.candidate.user.email],
            html_message=candidate_message,
            fail_silently=False,
        )

        # Send email to interviewer
        interviewer_subject = f"Reminder: Interview with {interview.candidate.user.get_full_name()}"
        interviewer_message = render_to_string(
            'emails/interview_reminder_interviewer.html',
            context
        )
        send_mail(
            interviewer_subject,
            interviewer_message,
            'noreply@recruiter.com',
            [interview.interviewer.email],
            html_message=interviewer_message,
            fail_silently=False,
        )

    except Interview.DoesNotExist:
        # Log error or handle as needed
        pass

@shared_task
def send_interview_feedback(interview_id):
    """
    Send feedback notification to the candidate after the interview.
    """
    try:
        interview = Interview.objects.get(id=interview_id)
        feedback = interview.interview_feedback

        context = {
            'interview': interview,
            'candidate_name': interview.candidate.user.get_full_name(),
            'job_title': interview.job.title,
            'feedback': feedback,
        }

        # Send feedback email to candidate
        subject = f"Interview Feedback for {interview.job.title}"
        message = render_to_string(
            'emails/interview_feedback.html',
            context
        )
        send_mail(
            subject,
            message,
            'noreply@recruiter.com',
            [interview.candidate.user.email],
            html_message=message,
            fail_silently=False,
        )

    except Interview.DoesNotExist:
        # Log error or handle as needed
        pass

@shared_task
def cleanup_old_interviews():
    """
    Clean up old completed interviews and their associated data.
    """
    # Get interviews completed more than 6 months ago
    cutoff_date = timezone.now() - timezone.timedelta(days=180)
    old_interviews = Interview.objects.filter(
        status='COMPLETED',
        updated_at__lt=cutoff_date
    )

    # Delete old interviews and their associated data
    for interview in old_interviews:
        interview.delete() 