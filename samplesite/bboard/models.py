from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    topic_title=models.CharField("Название темы", max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        #Возвращает название темы
        return self.topic_title
class Entry(models.Model):
    topic=models.ForeignKey(Topic,on_delete= models.CASCADE)
    entry_text=models.TextField("Entry")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Entries'
    def __str__(self):
        #Возвращает название темы
        return f"{self.entry_text[:50]}..."