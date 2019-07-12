from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import User

#TODO: sending view
class SendingView(generic.TemplateView):
    template_name = "assignment/sending.html"

class RegistrationView(generic.TemplateView):
    model = User
    template_name = "assignment/registration.html"

def register(request):
    user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password'],
    )
    return HttpResponseRedirect(reverse('assignment:sending'))
    # return render(request, 'assignment:sending')