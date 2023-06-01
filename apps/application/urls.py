from django.urls import path

from apps.application import views


urlpatterns = [
    path('client/applications/', views.ClientApplicationListAPIView.as_view()),
    path('client/application/create', views.ClientApplicationCreateAPIView.as_view()),

    # path('operator/appications/', views.OperatorApplicationListAPIView.as_view()),
    # path('operator/<int:pk>/', views.OperatorApplicationUpdateAPIView.as_view()),

    # path('brigade/applications/')
]
