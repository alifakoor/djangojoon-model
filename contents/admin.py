from django.contrib import admin

from .models import Post, Reaction, Tag, Comment


class CommentInlineAdmin(admin.TabularInline):
    model = Comment
    show_change_link = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInlineAdmin]
    list_display = (
        "owner",
        "short_content",
        "created_at",
        "like_count",
        "dislike_count",
    )
    list_filter = ["owner", "created_at"]
    search_fields = ["content"]

    def short_content(self, obj):
        return obj.content[:30] + "..." if len(obj.content) > 30 else obj.content

    short_content.short_description = "Content"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("owner", "post_content", "status")

    def post_content(self, reaction):
        content = reaction.post.content
        return content[:30] + "..." if len(content) > 30 else content


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("owner", "post_content", "content")

    def post_content(self, reaction):
        content = reaction.post.content
        return content[:30] + "..." if len(content) > 30 else content
