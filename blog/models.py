from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone


User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_profile = models.UUIDField(primary_key=True, default=uuid.uuid4)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(
        upload_to="profile_images", default="blank-profile-picture.png"
    )
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id_post = models.UUIDField(primary_key=True, default=uuid.uuid4)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images")
    title = models.TextField(blank=True)
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.profile.user.username


class UpvotePost(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    follower = models.CharField(max_length=100)
    followed = models.CharField(max_length=100)

    def __str__(self):
        return self.followed
