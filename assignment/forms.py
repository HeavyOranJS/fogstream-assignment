import logging
from smtplib import SMTPException

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone

from .models import MessageLog


class ContactForm(forms.Form):
    """
    Form for sending email to admin
    """
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    logger = logging.getLogger(__name__)

    def send_email(self, username=None):
        """
        Send email using the self.cleaned_data dictionary.
        Accepts current authorized user's username and uses it to sign
        email.
        """

        email = self.cleaned_data['email']
        message = self.cleaned_data['message']

        #get all superuser's emails in list
        staff_members = User.objects.filter(is_staff=True)
        staff_members_emails = [staff.email for staff in staff_members]

        successfully_sent = False
        try:
            if not staff_members_emails:
                raise ValueError("No superusers in system or they dont have emails")

            send_mail(
                subject="Message from user {}".format(username),
                message="Message:'{0}' \nEntered email: {1}".format(message, email),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=staff_members_emails
            )

        except SMTPException as ex:
            self.logger.error('Send_email error caused by %s', ex)
        except ValueError:
            self.logger.error("There is no staff members or none of them have emails")
        else:
            successfully_sent = True
        finally:
            MessageLog.objects.create_messagelog(username, timezone.now(), successfully_sent)
        return successfully_sent
