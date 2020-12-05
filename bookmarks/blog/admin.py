from django.contrib import admin

# Register your models here.
from .models import Blog,Comment,LikeDislike

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(LikeDislike)

# Register your models here.
