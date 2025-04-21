from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InterviewViewSet,
    InterviewQuestionViewSet,
    InterviewFeedbackViewSet
)

router = DefaultRouter()
router.register(r'interviews', InterviewViewSet, basename='interview')
router.register(r'questions', InterviewQuestionViewSet, basename='question')
router.register(r'feedback', InterviewFeedbackViewSet, basename='feedback')

urlpatterns = [
    path('', include(router.urls)),
] 