import datetime
from haystack import indexes
from .models import Profile


class ProfileIndex(indexes.SearchIndex):

    profile = indexes.CharField(model_attr='user')
    date_of_birth = indexes.DateTimeField(model_attr='date_of_birth')

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())