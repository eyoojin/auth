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

# 회원가입(Signup) 기능 구현

## 4. User modeling/migration
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
- migration

## 5. Signup - Create
- 경로 설정
```python
# auth/'urls.py'
from django.urls import path, include

path('accounts/', include('accounts.urls'))
```
```python
# accounts/'urls.py'
from django.urls import path, include
from . import views

app_name ='accounts'

urlpatterns = [path('signup/', views.signup, name='signup')]
```
- 함수 생성
```python
# accounts/'forms.py'
from .models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User
        # fields = '__all__'
        fields = ('username', )
        # password는 필수
```
```python
# views.py
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        pass
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'signup.html', context)
```
- 페이지 생성
```html
<!-- accounts/templates/'signup.html' -->
{% extends 'base.html' %}

{% block body %}
    <form action="" method="POST">
        {% csrf_token %}
        {{form}}
        <input type="submit">
    </form>
{% endblock %}
```
- 회원가입 정보 저장
```python
# views.py
from django.shortcuts import redirect

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
```
- validation check (유효성 검사)
    - `if form.is_valid():`에서 처리
    - 비밀번호가 너무 짧거나 흔하거나 등등

- 암호화
    - 평문을 난수로 바꿈
    - hash 함수
        - 어떠한 계산의 결과
        - sha1: 결과를 보고 원본을 유추 가능
        - sha256: 현재 쓰는 암호화 함수
    - salt
        - 사람마다 다른 랜덤한 문자열을 추가로 붙임 -> 똑같은 비밀번호를 쓰더라도 다르게 저장됨

# 로그인 기능 구현

1. User가 ID와 PW를 server로 보냄
2. ID/PW가 가지고 있는 데이터와 일치하는지 확인
3. User Session(임의의 난수) 키 발급 -> **Create**
4. Session을 cookies에 저장

- 쿠키를 허용함: 브라우저의 일정 공간에 데이터를 저장하도록 허용함

## 6. Login - Create
- 경로 설정
```python
# urls.py
path('login/', views.login, name='login')
```
- 함수 생성
```python
# forms.py
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    pass
```
```python
# views.py
from .forms import CustomAuthenticationForm

def login(request):
    if request.method == 'POST':
        pass
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'login.html', context)
```
- 페이지 생성
```html
<!-- login.html -->
<form action="" method="POST">
    {% csrf_token %}
    {{form}}
    <input type="submit">
</form>
```
- user session 발급
```python
# views.py
from django.contrib.auth import login as auth_login
# django가 이미 만들어둔 login함수가 우리 함수와 이름이 같기 때문에 다르게 설정

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        # request.POST: ID, PW 정보
        if form.is_valid():
            auth_login(request, form.get_user())
            # form.get_user(): 유저 데이터(ID, PW)
            # login: 세션 발급해주는 함수
            return redirect('articles:index')
```