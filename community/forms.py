from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ['title', 'movie_title', 'rank', 'content']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'my-content',
                'rows': 1,
                'cols': 70,
                'placeholder': '댓글을 입력하세요.'
            }
        )
    )
    class Meta:
        model = Comment
        exclude = ['review', 'user']
