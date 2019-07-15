from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import FormView

from .forms import ContactForm


class ContactView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """
    Send a message to admin. Requires login
    """
    #use custom imported form
    form_class = ContactForm
    #override default template name
    template_name = "assignment/contact.html"
    
    #override default login page location, triggers if unauthorised user
    #tried to access this page (LoginRequiredMixin)
    login_url = '/assignment/login/'
    success_url = '/assignment/login/'
    success_message = "Email sent successfully"

    def form_valid(self, form):
        #send email from form, get message if it was successful
        email_sent_successfully = form.send_email(self.request.user.username)
        if not email_sent_successfully:
            self.success_message = "Email was not sent, please try again later"
        return super().form_valid(form)

class SignupView(FormView):
    """
    Sign up new users
    """

    #use template form for user creation
    form_class = UserCreationForm
    #override default template name
    template_name = "assignment/signup.html"

    #if form is valid
    def form_valid(self, form):
        form.save()
        #get data from form
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')
        #create new user
        #TODO: exception on authenticate from auth tutorial
        user = authenticate(username=username, raw_password=raw_password)
        #log in new user in his new account
        login(self.request, user)
        #redirect to contact page, because there is nothing to do in this app
        return redirect(reverse('assignment:contact'))

class LoginView(FormView):
    """
    Log in existing users
    """
<<<<<<< HEAD
    
=======
>>>>>>> ac6d4017b909c2d7af099c87dbf014326b0b6616
    #TODO: if not logged in user was redirected here from
    # contact view, show message like "you must be logged in to send messages"

    form_class = AuthenticationForm
    template_name = 'assignment/login.html'
    success_url = 'assignment/contact.html'

    #if form is valid
    def form_valid(self, form):
        #no exception because form handles it
        #login user data from form
        login(self.request, form.get_user())
        return redirect(reverse('assignment:contact'))
