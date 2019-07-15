from smtplib import SMTPException
from django.utils import timezone

from django import forms
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import MessageLog


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

        superusers = User.objects.filter(is_superuser=True)
        superusers_emails = [superuser.email for superuser in superusers]
        
        successfully_sent = False
        try:
            if not superusers_emails:
                raise ValueError("No superusers in system or they dont have emails")
            
            send_mail(
                subject="Message from user {}".format(username),
                message="Message:'{0}' \nEntered email: {1}".format(message, email),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=superusers_emails
            )

        except SMTPException as ex:
            pass
        except ValueError as ex:
            print(ex)
        else:
            successfully_sent = True
        finally:
            MessageLog.objects.create_messagelog(username, timezone.now(), successfully_sent)
        return successfully_sent
        