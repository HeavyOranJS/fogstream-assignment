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
        Send email using the self.cleaned_data dictionary
        """

        email = self.cleaned_data['email']
        message = self.cleaned_data['message']

        mail_admins(subject="message from user {}".format(username), message=message)