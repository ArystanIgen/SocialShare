from django import forms
from .models import Blog,Comment
from bootstrap_modal_forms.forms import BSModalModelForm

class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['blog_text','photo']
        labels = {'blog_text':''}
        widgets = {'text': forms.Textarea(attrs={'cols': 40})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('cooment_text',)

class CommentModelForm(BSModalModelForm):
    class Meta:
        model = Comment
        fields = ['cooment_text']
class Search1Form(forms.Form):
    query = forms.CharField()