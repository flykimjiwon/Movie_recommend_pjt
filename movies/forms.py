from django import forms
from movies.models import MovieComment

class MovieCommentForm(forms.ModelForm):
    rank_choices = ((5, '★★★★★'),(4, '★★★★'),(3, '★★★'),(2, '★★'),(1, '★'))
    rank = forms.ChoiceField(
        label='',
        choices=rank_choices,
        widget=forms.Select(),
        required=True
    )
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'my-content',
                'rows': 1,
                'cols': 70,
                'placeholder': '한줄평을 작성해주세용!'
            }
        ),
        required=True
    )
    class Meta:
        model = MovieComment
        fields = ('content', 'rank')
        # exclude = ('movie', 'user',)