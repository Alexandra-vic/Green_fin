from django.urls import path
from apps.application.views import (
    ApplicationCreateAPIView,
    ApplicationListAPIView,
    ApplicationDetailView,
)


urlpatterns=[
    path('application/create/', ApplicationCreateAPIView.as_view()),
    path('applications/', ApplicationListAPIView.as_view()),
    path('application/<int:pk>/', ApplicationDetailView.as_view()),
]
