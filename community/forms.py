from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
        label='글 제목',
        widget=forms.TextInput(
            attrs={
                'placeholder': ' 제목을 입력하세요.',
            }
        ),
        required=True
    )
    content = forms.CharField(
        label='글 내용',
        widget=forms.Textarea(
            attrs={
                'placeholder': ' 내용을 입력하세요.',
                'cols': 100,
            }
        ),
        required=True
    )
    class Meta:
        model = Review
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'rows': 1,
                'cols': 70,
                'placeholder': '댓글을 입력하세요.'
            }
        ),
        required=True
    )
    class Meta:
        model = Comment
        exclude = ['review', 'user']
