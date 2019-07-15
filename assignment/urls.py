from django.urls import path

from . import views

app_name = 'assignment'

urlpatterns = [
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.SignupView.as_view(), name='signup'),
]
