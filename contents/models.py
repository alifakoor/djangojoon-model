from django.core.validators import FileExtensionValidator
from django.db import models


REACTION_CHOICES = (("1", "like"), ("2", "dislike"))


def get_upload_path(instance, filename):
    return f"user_{instance.owner.id}/{filename}"


class Tag(models.Model):
    name = models.CharField(max_length=128)


class Post(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    image = models.FileField(
        upload_to=get_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg"])],
        blank=True,
        null=True,
    )
    content = models.TextField()
    tags = models.ManyToManyField("Tag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def like_count(self):
        return self.reactions.filter(status="1").count()

    def dislike_count(self):
        return self.reactions.filter(status="2").count()


class Reaction(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    status = models.CharField(choices=REACTION_CHOICES, max_length=1)

    class Meta:
        unique_together = ("owner", "post")


class Comment(models.Model):
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.reply_to:
            self.post = self.reply_to.post
        super().save(force_insert, force_update, using, update_fields)
