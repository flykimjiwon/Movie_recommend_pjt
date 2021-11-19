from django import forms
from movies.models import MovieComment

class MovieCommentForm(forms.ModelForm):

    class Meta:
        model = MovieComment
        exclude = ('movie', 'user',)