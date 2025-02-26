from django.contrib import admin
from django.contrib.sessions.models import Session
from userauth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email','bio']
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'decoded_data', 'expire_date']
    readonly_fields = ['session_key', 'decoded_data', 'expire_date']
    ordering = ['-expire_date']

    def decoded_data(self, obj):
        return obj.get_decoded()

    decoded_data.short_description = "Session Data"

admin.site.register(Session,SessionAdmin)
admin.site.register(User,UserAdmin)
