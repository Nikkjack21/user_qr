from django.contrib import admin
from accounts.models import Accounts, ShortenURL
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ("full_name", "email", "url")

    def url(self, obj):
        url_list = ", ".join([
            url.shorten_url for url in obj.urls.all()
        ])
        return  url_list
    
    ordering = ("email",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(ShortenURL)
admin.site.register(Accounts, AccountAdmin)
