from django.contrib import admin
from .models import BlogPost,comment

admin.site.register(BlogPost)
admin.site.register(comment)