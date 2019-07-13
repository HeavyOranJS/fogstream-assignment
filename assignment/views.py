from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic


#TODO: sending view
class SendingView(LoginRequiredMixin, generic.TemplateView):
    """
    Send a message to admin. Requires login
    """
    #TODO change login_url
    # to redirect mixin to correct login page if user is not logged in
    login_url = '/assignment/login/'
    template_name = "assignment/sending.html"


class SignupView(generic.edit.FormView):
    """
    Sign up new users
    """
    #TODO: link to login page
    
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
        #redirect to sending page, because there is nothing to do in this app
        return redirect(reverse('assignment:sending'))


class LoginView(generic.edit.FormView):
    """
    Log in existing users
    """
    #TODO: link to signup page
    #TODO: if not logged in user was redirected here from
    # sending view, show message like "you must be logged in to send messages"
    
    form_class = AuthenticationForm
    template_name = 'assignment/login.html'
    success_url = 'assignment/sending.html'
    
    #if form is valid
    def form_valid(self, form):
        #no exception because form handles it
        #login user data from form
        login(self.request, form.get_user())
        return redirect(reverse('assignment:sending'))
