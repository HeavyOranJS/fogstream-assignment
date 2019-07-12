from django.urls import path
from . import views

app_name = 'assignment'

urlpatterns = [
    path('sending/', views.SendingView.as_view(), name='sending'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('register/', views.register, name='register'),
]