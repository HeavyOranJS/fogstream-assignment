from django.contrib import admin
from .models import MessageLog

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    """
    Settings for MessageLog section of admin dashboard
    """
    fieldsets = [
        (None, {'fields': ['sender', 'status']}),
        ('Date information', {
            'fields': ['time']
            }
        )
    ]

    list_display = (
        'sender',
        'time',
        'status',
    )
