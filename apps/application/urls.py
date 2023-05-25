from django.urls import path
from apps.application.views import (
    ClientApplicationListAPIView,
    ClientApplicationCreateAPIView,
    OperatorApplicationListAPIView,
    OperatorApplicationUpdateAPIView,
    BrigadeApplicationListAPIView,
    BrigadeApplicationUpdateAPIView,
)


urlpatterns=[
    path('client/applications/', ClientApplicationListAPIView.as_view()),
    path('client/application/create', ClientApplicationCreateAPIView.as_view()),

    path('operator/appications/', OperatorApplicationListAPIView.as_view()),
    path('operator/<int:pk>/', OperatorApplicationUpdateAPIView.as_view()),

    path('brigade/applications/')
]
