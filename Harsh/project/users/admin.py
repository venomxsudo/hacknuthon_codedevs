from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, PendingUser, Query

admin.site.register(User,UserAdmin)
admin.site.register(PendingUser)
admin.site.register(Query)
admin.site.site_header = 'Online_Assignment'
admin.site.index_title = 'Admin Dashboard'

