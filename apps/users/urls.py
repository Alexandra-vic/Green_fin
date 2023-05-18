from django.urls import path, include

from apps.users import views
from rest_framework import routers

app_name = 'users'


router = routers.DefaultRouter()
router.register(r'operators', views.OperatorViewSet)
router.register(r'brigades', views.BrigadeViewSet)
router.register(r'clients', views.ClientViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('resetpassword/', views.ResetPasswordAPIView.as_view()),
]
