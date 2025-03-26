from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # 상속받아왔기 때문에 코드는 필요 없음
    pass