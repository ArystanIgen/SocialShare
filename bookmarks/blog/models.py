from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.db.models import Sum
class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def blogs(self):
        return self.get_queryset().filter(content_type__model='blog')

    def comments(self):
        return self.get_queryset().filter(content_type__model='comment')
class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name=("Голос"), choices=VOTES)
    user = models.ForeignKey(User, verbose_name=("Пользователь"),on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_text=models.TextField("What's up on your mind")
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    votes = GenericRelation(LikeDislike, related_query_name='blogs')
    headline = models.CharField(max_length=500)

    def was_published_recently(self):
        return self.date_added>=(timezone.now()-datetime.timedelta(days=7))





class Comment(models.Model):
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE,related_name="comments")
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    cooment_text=models.TextField("Comment")
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    votes = GenericRelation(LikeDislike, related_query_name='comments')


