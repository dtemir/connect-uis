from django.contrib import admin
from .models import Profile, Post, UpvotePost, Follow


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(UpvotePost)
admin.site.register(Follow)
