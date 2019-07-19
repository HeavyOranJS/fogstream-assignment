import json
import logging
from smtplib import SMTPException
from urllib import request

import requests
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

    #url for searchin user by email
    URL = "http://jsonplaceholder.typicode.com/users"

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

            final_message = ("Message:'{}' \n".format(message) \
                + "Entered email: {} \n".format(email) \
                + self.get_email_info(self.URL, email))

            send_mail(
                subject="Message from user {}".format(username),
                message=final_message,
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

    def pritify_json(self, record, indent=""):
        """
        Returns pretty parsed text from json-like dictionary
        """
        parsed_record = ""
        for key, value in record.items():
            if isinstance(value, dict):
                parsed_record += indent + "{}:\n".format(key)
                parsed_record += self.pritify_json(value, "    ")
                continue
            parsed_record += indent + "{}: {}\n".format(key, value)
        return parsed_record

    def get_email_info(self, url, email):
        """
        Make request to url, fetch JSON data, get record with
        specified email and return pretty text of this record
        """
        parsed_data = requests.get(url).json()

        #find first entry of user with email
        record_with_email = next(record for record in parsed_data if record['email'] == email)
        return self.pritify_json(record_with_email)
