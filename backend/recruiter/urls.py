from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_auth.urls')),
    path('api/auth/registration/', include('rest_auth.registration.urls')),
    path('api/candidates/', include('recruiter.apps.candidates.urls')),
    path('api/jobs/', include('recruiter.apps.jobs.urls')),
    path('api/interviews/', include('recruiter.apps.interviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 