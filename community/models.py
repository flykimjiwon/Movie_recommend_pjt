from django.db import models
from django.conf import settings


class Review(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(null=True)
    # 이거 넣어주기
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(null=True)
    # 이거 넣어주기 null=True
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content
