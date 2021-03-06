from .models import Movies
from django import forms


class MoviesForm(forms.ModelForm):
    class Meta:
        model = Movies
        # fields = ["title", "url", "youtube_id"]
        fields = ["url"]
        labels = {"url": "YouTube Url:"}


class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label="Search for Videos:")
