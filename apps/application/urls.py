from django.urls import path
from apps.application.views import (
    ClientApplicationListAPIView,
    ClientApplicationCreateAPIView,
    ApplicationListAPIView,
    ApplicationUpdateView,
    AssignBrigadeView,
    UpdateApplicationStatusView,

    # OperatorApplicationUpdateAPIView,
)


urlpatterns=[
    path('client/applications/', ClientApplicationListAPIView.as_view()),
    path('client/application/create', ClientApplicationCreateAPIView.as_view()),

    path('applications/', ApplicationListAPIView.as_view()),
    path('operator/<int:pk>/my_applications/', ApplicationUpdateView.as_view()),
    path('choice_brigade/<int:pk>/', AssignBrigadeView.as_view()),

    path('brigade/<int:pk>/change_status/', UpdateApplicationStatusView.as_view()),
    # path('operator/<int:pk>/', OperatorApplicationUpdateAPIView.as_view()),

]
