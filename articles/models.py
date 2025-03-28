from django.db import models
from accounts.models import User # 1.
from django.conf import settings # 2.
from django.contrib.auth import get_user_model # 3.

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    # 1. 직접참조 -> 추천하지 않음
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 2. settings.py 변수 활용
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 3. get_user_model
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)