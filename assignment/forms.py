from django import forms
from django.conf import settings
from django.core.mail import mail_admins, send_mail


class SendingForm(forms.Form):
    """
    Form for sending email to admin
    """
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    #TODO: prepopulate email field
    #TODO: send email

    def send_email(self, username=None):
        """
        Send email using the self.cleaned_data dictionary
        """
        #TODO: remove print
        email = self.cleaned_data['email']
        message = self.cleaned_data['message']

        mail_admins(subject="message from user {}".format(username), message=message)
        # send_mail("test subject", message, "test from email", recipient_list=["tess"] )
        # send_mail(message=message, receiver=receiver)
