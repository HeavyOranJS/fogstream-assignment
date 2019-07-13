from django.urls import path
from . import views

app_name = 'assignment'

urlpatterns = [
    path('sending/', views.SendingView.as_view(), name='sending'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
]