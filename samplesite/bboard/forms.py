from django import forms
from .models import Topic,Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['topic_title']
        labels = {'topic_title':''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_text']
        labels = {'entry_text': 'Entry:'}
        widgets = {'entry_text': forms.Textarea(attrs={'cols': 80})}