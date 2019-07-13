from django import forms
from django.conf import settings
from django.core.mail import mail_admins, send_mail


class ContactForm(forms.Form):
    """
    Form for sending email to admin
    """
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self, username=None):
        """
        Send email using the self.cleaned_data dictionary.
        Accepts current authorized user's username and uses it to sign
        email.
        """

        email = self.cleaned_data['email']
        message = self.cleaned_data['message']

        mail_admins(
            subject="Message from user {}".format(username), 
            message="Message:'{0}' \nEntered email: {1}".format(message, email)
        )
