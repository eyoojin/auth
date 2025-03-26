# auth
- 로그인 관련 기능
    - authentication >> 인증
    - authorization

- 프로젝트를 만들 때
    - 데이터베이스의 **구조 설계**를 먼저 하는 것이 좋음
        - 무슨 데이터를 저장하고 싶은지
        - 데이터끼리 어떤 상관관계를 가지는지

- 오늘 프로젝트의 구조
    - User -< Post
    - User -< Comment
    - Post -< Comment

## 0. .gitignore 설정
- 가상환경 생성/ 활성화
- django 설치
- .gitignore 설정

## 1. startproject

## 2. startapp accounts
- settings.py

## 3. base.html
- ../templates/
- settins.py
```python
# settings.py
TEMPLATES = [{'DIRS': [ BASE_DIR / 'templates' ]}]
```
- bootstrap 적용
```html
<!-- base.html -->
<div class="container">
    {% block body %}
    {% endblock %}
</div>
```

## 4. User modeling/ migrate
```python
# models.py
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 상속받아왔기 때문에 코드는 필요 없음
    pass
```
- Django는 원래 사용하던 User 모델이 있기 때문에 내가 새로 만든 것과 충돌이 일어날 수 있음 -> Django에게 내가 만든 모델로 사용하겠다고 말해줘야 함
```python
# settings.py
AUTH_USER_MODEL = 'accounts.User'
```
- migrations