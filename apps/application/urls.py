from django.urls import path
from apps.application import views

urlpatterns=[
    path('client/application/create/', views.ClientApplicationCreateAPIView.as_view()),

    path('applications/', views.ApplicationListAPIView.as_view()),
    path('operator/<int:pk>/my_applications/', views.AssignOperatorAPIView.as_view()),

    path('brigades/', views.BrigadeListAPIView.as_view(), name='brigade-list'),
    path('add_brigade/<int:pk>/', views.AddBrigadeAPIView.as_view()),
    path('brigade/<int:pk>/status/', views.BrigadeStatusUpdateView.as_view()),
    path('in_progressing_status/<int:pk>/', views.BrigadeApplicationStatusUpdateAPIView.as_view()),

    path('change_status/<int:pk>/', views.ApplicationStatusUpdateAPIView.as_view()),
]
