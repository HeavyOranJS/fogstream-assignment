from django.db import models

class MessageLogManager(models.Manager):
    """
    Manager for MessageLog. Handles creation of new MessageLog objects
    """
    def create_messagelog(self, sender, time, status):
        """
        Create new MessageLog object
        """
        messagelog = self.create(sender=sender, time=time, status=status)
        return messagelog

class MessageLog(models.Model):
    """
    Stores data about sent emails: username of sender, time and boolean
    status (True = success, False = failure)
    """
    #username
    sender = models.CharField(max_length=200)
    time = models.DateTimeField('date of sending')

    #bind manager
    objects = MessageLogManager()

    #was email send successfully
    status = models.BooleanField()

    def __str__(self):
        return "sender: {}, time: {}, status:{}".format(
            self.sender,
            self.time,
            self.status
        )
