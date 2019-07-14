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
    #username assumed
    sender = models.CharField(max_length=200)
    time = models.DateTimeField('sending date')
    #was email send successfully
    status = models.BooleanField('Sent successfully')

    #bind manager
    objects = MessageLogManager()

    #override standard __str__ function to display relevant info about object
    def __str__(self):
        return "sender: {}, time: {}, status:{}".format(
            self.sender,
            self.time,
            self.status
        )
