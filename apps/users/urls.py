from django.urls import path

from apps.users import views

app_name = 'users'


urlpatterns = [
    path('operators/', views.OperatorListView.as_view(), name='operator-list'),
    path('operators/register', views.OperatorRegisterView.as_view(), name='operator-reg'),
    path('operators/<int:pk>/', views.OperatorDetailView.as_view(), name='operator-detail'),

    path('brigades/', views.BrigadeListView.as_view(), name='brigade-list'),
    path('brigades/<int:pk>/', views.BrigadeDetailView.as_view(), name='brigade-detail'),
    path('brigades/register/', views.BrigadeRegisterView.as_view(), name='brigade-reg'),

    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('clients/register/', views.ClientRegisterView.as_view(), name='client-reg'),

    path('login/', views.UserLoginView.as_view(), name='login'),
    path('resetpassword/', views.ResetPasswordAPIView.as_view(), name='reset-password'),
]
