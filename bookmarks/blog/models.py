from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_text=models.TextField("What's up on your mind")
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    def was_published_recently(self):
        return self.date_added>=(timezone.now()-datetime.timedelta(days=7))

class Comment(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE,related_name="comments")
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cooment_text=models.TextField("Comment")
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)