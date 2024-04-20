from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, PendingUser, QueryModel, ChatHistory, QueryRun

from django.contrib import admin
from .models import ChatHistory

class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_query', 'generated_sql_query')  # Display fields in the list view
    list_filter = ('user',)  # Enable filtering by user

admin.site.register(ChatHistory, ChatHistoryAdmin)

admin.site.register(User,UserAdmin)
admin.site.register(PendingUser)
admin.site.register(QueryModel)
admin.site.register(QueryRun)
# admin.site.register(Query)
admin.site.site_header = 'Code Devs Admin'
admin.site.index_title = 'Admin Dashboard'

