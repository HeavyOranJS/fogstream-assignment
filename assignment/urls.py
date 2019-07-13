from django.urls import path

from . import views

app_name = 'assignment'

urlpatterns = [
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
]
