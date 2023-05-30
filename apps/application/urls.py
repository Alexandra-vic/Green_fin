from django.urls import path
from apps.application.views import (
    ClientApplicationListAPIView,
    ClientApplicationCreateAPIView,
    ApplicationListAPIView,
    AssignOperatorAPIView,
    BrigadeListAPIView,
    AddBrigadeAPIView,
    BrigadeApplicationsAPIView,
    ApplicationStatusUpdateAPIView,
)


urlpatterns=[
    path('client/application/create/', ClientApplicationCreateAPIView.as_view()),
    path('client/applications/', ClientApplicationListAPIView.as_view()),

    path('applications/', ApplicationListAPIView.as_view()),
    path('operator/<int:pk>/my_applications/', AssignOperatorAPIView.as_view()),

    path('brigades/', BrigadeListAPIView.as_view(), name='brigade-list'),
    path('add_brigade/<int:pk>/', AddBrigadeAPIView.as_view()),
    path('brigade/applications/', BrigadeApplicationsAPIView.as_view()),
    path('change_status/<int:pk>/', ApplicationStatusUpdateAPIView.as_view()),
]
