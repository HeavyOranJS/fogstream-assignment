from django.contrib import admin
from .models import MessageLog

@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    # fields = ['sender login', 'time sent', 'status']
    # fieldsets = [
    #     ('sender login', 'sender'),
    #     ('time sent', 'time'),
    #     ('is successful', 'status'),
    # ]

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