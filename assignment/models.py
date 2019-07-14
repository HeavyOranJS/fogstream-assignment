from django.db import models

class MessageLog(models.Model):
    """
    Stores data about sent emails: username of sender, time and boolean
    status (True = success, False = failure)
    """
    #username
    sender = models.CharField(max_length=200)
    time = models.DateTimeField('date of sending')
    #was email send successfully
    status = models.BooleanField()
