from django.contrib import admin
from accounts.models import Accounts, ShortenURL
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ("id","full_name", "email", "url", "visits")
    def url(self, obj):
        url_list = ", ".join([
            url.shorten_url for url in obj.urls.all()
        ])
        return  url_list
    
    def visits(self, obj):
        for url in obj.urls.all():
            return url.visited_count
    
    ordering = ("email",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



class URLAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ShortenURL._meta.get_fields()]
    readonly_fields = ("visited_count", "shorten_url", "token")
    list_display_links = ["user"]

admin.site.register(Accounts, AccountAdmin)
admin.site.register(ShortenURL, URLAdmin)
