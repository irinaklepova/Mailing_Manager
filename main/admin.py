from django.contrib import admin

from main.models import Client, Message, Mailing, Log


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'email',)
    list_filter = ('last_name', 'first_name', 'email',)
    search_fields = ('last_name', 'first_name', 'email', 'comment',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', 'text',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'periodicity', 'status', 'letter',)
    list_filter = ('start_time', 'end_time', 'periodicity', 'status', 'letter',)
    search_fields = ('start_time', 'end_time', 'periodicity', 'status', 'letter',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('last_attempt_time', 'attempt_status', 'server_response', 'mailing',)
    search_fields = ('last_attempt_time', 'attempt_status', 'server_response', 'mailing',)
