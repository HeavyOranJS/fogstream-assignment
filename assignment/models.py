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

    class Meta:
        verbose_name = "Message sent to staff"
        verbose_name_plural = "Messages sent to staff"

    #assumes username
    sender = models.CharField("Sender's username", max_length=200)
    time = models.DateTimeField("Date the message was sent")
    #was email sent successfully
    status = models.BooleanField("Sent successfully")

    #bind manager
    objects = MessageLogManager()


    def __str__(self):
        return "sender: {}, time: {}, status:{}".format(
            self.sender,
            self.time,
            self.status
        )
