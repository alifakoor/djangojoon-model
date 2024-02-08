from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "display_name",
        "is_active",
        "get_following_count",
        "get_followers_count",
    )
    list_filter = ["is_active"]
    search_fields = ["username"]

    def display_name(self, obj):
        return obj.display_name()

    display_name.short_description = "Full Name"

    def get_following_count(self, obj):
        return obj.followings.count()

    get_following_count.short_description = "Following Count"

    def get_followers_count(self, obj):
        return User.objects.filter(followings=obj).count()

    get_followers_count.short_description = "Followers Count"
