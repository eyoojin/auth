# auth
- 로그인 관련 기능
    - authentication >> 인증
    - authorization

- 프로젝트를 만들 때
    - 데이터베이스의 **구조 설계**를 먼저 하는 것이 좋음
        - 무슨 데이터를 저장하고 싶은지
        - 데이터끼리 어떤 상관관계를 가지는지

- 오늘 프로젝트의 구조
    - User -< Article
    - User -< Comment
    - Article -< Comment

## 0. .gitignore 설정
- 가상환경 생성/ 활성화
- django 설치
- .gitignore 설정

## 1. startproject

## 2. startapp accounts
- settings.py

## 3. base.html
```python
# auth/'settings.py'
TEMPLATES = [{'DIRS': [ BASE_DIR / 'templates' ]}]
```
- bootstrap 적용
```html
<!-- ../templates/'base.html' -->
<div class="container">
    {% block body %}
    {% endblock %}
</div>
```

# 회원가입/로그인/로그아웃

## 4. User modeling/migration
```python
# accounts/'models.py'
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 상속받아왔기 때문에 코드는 필요 없음
    pass
```
- Django는 원래 사용하던 User 모델이 있기 때문에 내가 새로 만든 것과 충돌이 일어날 수 있음 -> Django에게 내가 만든 모델로 사용하겠다고 말해줘야 함
```python
# auth/'settings.py'
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
# accounts/'views.py'
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
# accounts/'views.py'
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
---
- 암호화
    - 평문을 난수로 바꿈
    - hash 함수
        - 어떠한 계산의 결과
        - sha1: 결과를 보고 원본을 유추 가능
        - sha256: 현재 쓰는 암호화 함수
    - salt
        - 사람마다 다른 랜덤한 문자열을 추가로 붙임 -> 똑같은 비밀번호를 쓰더라도 다르게 저장됨

## 6. Login - Create
1. User가 ID와 PW를 server로 보냄
2. ID/PW가 가지고 있는 데이터와 일치하는지 확인
3. User Session(임의의 난수) 키 발급 -> **Create**
4. Session을 cookies에 저장

- 쿠키를 허용함: 브라우저의 일정 공간에 데이터를 저장하도록 허용함
---
- 경로 설정
```python
# accounts/'urls.py'
path('login/', views.login, name='login')
```
- 함수 생성
```python
# accounts/'forms.py'
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    pass
```
```python
# accounts/'views.py'
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
<!-- accounts/templates/'login.html' -->
<form action="" method="POST">
    {% csrf_token %}
    {{form}}
    <input type="submit">
</form>
```
- user session 발급
```python
# accounts/'views.py'
from django.contrib.auth import login as auth_login
# django가 이미 만들어둔 login함수가 우리 함수와 이름이 같기 때문에 다르게 설정

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        # request.POST: ID, PW 정보가 담긴
        if form.is_valid():
            auth_login(request, form.get_user())
            # form.get_user(): 유저 데이터(ID)
            # auth_login: 세션 발급해주는 함수
            return redirect('articles:index')
```
- login 성공
```html
<!-- ../templates/'base.html' -->
<nav class="nav">
    <!-- {{user}}: context에 담지 않아도 이미 가지고 있는 변수 -->
    <a href="" class="nav-link disabled">{{user}}</a>
    <a href="{% url 'accounts:signup' %}" class="nav-link">signup</a>
    <a href="{% url 'accounts:login' %}" class="nav-link">login</a>
    <a href="{% url 'accounts:logout' %}" class="nav-link">logout</a>

</nav>
```

## 7. Logout - Delete

- 데이터베이스에서 session을 찾아서 지워줌
---
```python
# accounts/'urls.py'
path('logout/', views.logout, name='logout')
```
```python
# accounts/'views.py'
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('accounts:login')
```

## 8. 로그인 유무에 따른 nav 구조 변경
```html
<!-- ../templates/'base.html' -->
<nav class="nav">
    <!-- is => True or False -->
    {% if user.is_authenticated %}
        <a href="" class="nav-link disabled">{{user}}</a>
        <a href="{% url 'accounts:logout' %}" class="nav-link">logout</a>
    {% else %}
        <a href="{% url 'accounts:signup' %}" class="nav-link">signup</a>
        <a href="{% url 'accounts:login' %}" class="nav-link">login</a>        
    {% endif %}
</nav>
```

# 게시물 생성

## 9. startapp articles
- settings.py

## 10. Article modeling/migration
```python
# articles/'models.py'

# 1. 직접참조 -> 추천하지 않음
from accounts.models import User
user = models.ForeignKey(User, on_delete=models.CASCADE)

# 2. settings.py 변수 활용
from django.conf import settings
user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# 3. get_user_model
from django.contrib.auth import get_user_model
user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
```

## 11. Article - Create
```python
# auth/'urls.py'
path('articles/', include('articles.urls'))
```
```python
# articles/'urls.py'
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [path('', views.index, name='index')]
```
```python
# articles/'views.py'
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
```
```html
<!-- articles/templates/'index.html' -->
{% extends 'base.html' %}

{% block body %}
    <h1>index</h1>
{% endblock %}
```
```html
<!-- ../templates/'base.html' -->
<a href="{% url 'articles:create' %}" class="nav-link">create</a>
```
```python
# articles/'urls.py'
path('create/', views.create, name='create')
```
```python
# articles/'forms.py'
from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta():
        model = Article
        fields = '__all__'
```
```python
# articles/'views.py'
from .forms import ArticleForm

def create(request):
    if request.method == 'POST':
        pass
    else:
        form = ArticleForm()
    
    context = {
        'form': form,
    }

    return render(request, 'create.html', context)
```
```html
<!-- articles/templates/'create.html' -->
<form action="" method="POST">
    {% csrf_token%}
    {{form}}
    <input type="submit">
</form>
```
```python
# articles/'forms.py'
# fields or exclude
# fields = '__all__'
fields = ('title', 'content', )
exclude = ('user', )
```
```python
# articles/'views.py'
from django.shortcuts import redirect

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            # user 정보를 직접 넣어줘야함
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')
```

## 12. Article - Read
```python
# articles/'views.py'
from .models import Article

def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)
```
```html
<!-- articles/templates/'index.html' -->
{% for article in articles %}
    <h3>{{article.title}}</h3>
    <p>{{article.content}}</p>
    <p>{{article.user}}</p>
    <hr>
{% endfor %}
```

## 13. login_required
```python
# articles/'views.py'
from django.contrib.auth.decorators import login_required

# decorator: 아래에 있는 함수를 실행하기 전에 위의 함수를 먼저 실행해주세요
@login_required # 로그인을 해야 접근 가능
def create(request):
```
- 흐름 수정
```python
# accounts/'views.py'
def login(request):
    return redirect('articles:index')
```

## 14. next 인자 처리하기
```python
def login(request):
    # /accounts/login/
    # /accounts/login/?next=/articles/create/
    next_url = request.GET.get('next')

    # next가 없을 때 => None or 'articles:index'
    # next가 있을 때 => '/articles/create/' or 'articles:index'
    return redirect(next_url or 'articles:index')
```
- or
    - 둘 중에 하나라도 1이면 1
    - 단축평가
        - 앞 True => 앞 반환
        - 앞 False => 뒤 반환

# 댓글 기능

## 15. Comment modeling/migration

```python
# articles/'models.py'
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
```
- migration

## 16. Article Read 1

- 댓글 구현 전에 보여주는 페이지 먼저 만듦

```html
<!-- articles/templates/'index.html' -->
<a href="{% url 'articles:detail' article.id %}">detail</a>

```
```python
# articles/'urls.py'
path('<int:id>/', views.detail, name='detail')
```
```python
# articles/templates/'views.py'
def detail(request, id):
    article = Article.objects.get(id=id)

    context = {
        'article': article,
    }

    return render(request, 'detail.html', context)
```
```html
<!-- articles/templates/'detail.html' -->
{% extends 'base.html' %}

{% block body %}
    <h1>{{article.title}}</h1>
    <p>{{article.content}}</p>
    <p>{{article.user}}</p>
{% endblock %}
```

## 17. Comment Create

- CommentForm 정의
- CommentForm 불러오기
- CommentForm 인스턴스화

```python
# articles/'forms.py'
from .models import Comment

class CommentForm(ModelForm):
    class Meta():
        model = Comment
        fields = '__all__'
```
```python
# articles/'views.py'
from .forms import CommentForm

def detail(request, id):
    form = CommentForm()
    # 댓글 보여주는 기능(get요청)

    context = {
        'form': form,
    }
```
```html
<!-- articles/templates/'detial.html' -->
<hr>
<form action="" method="POST">
    {% csrf_token %}
    {{form}}
    <input type="submit">
</form>
```
- content만 보이도록 수정
```python
# articles/'forms.py'
fields = ('content', )
```
- action 설정
```html
<!-- articles/templates/'detail.html' -->
<form action="{% url 'articles:comment_create' article.id %}">
```
- url 설정
```python
# articles/'urls.py'
path('<int:article_id>/comments/create/', views.comment_create, name='comment_create')
```
- 함수 생성
```python
# articles/'views.py'
@login_required
def comment_create(request, article_id):
    # if request.method == 'POST':
    #     pass
    # else:
    #     pass
    # 댓글 작성에는 get요청이 들어오지 않기 때문에 if문 안쪽의 코드만 있으면 됨
    # 댓글 작성칸을 보여주는 건 detail 함수에서 함

    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)

        # 객체를 저장하는 경우
        comment.user = request.user # 유저 정보 = 현재 로그인한 사람
        article = Article.objects.get(id=article_id) # 게시물 정보 = 현재 게시글
        comment.article = article

        # id 값을 저장하는 경우
        # DB에 저장되는 숫자를 가져옴
        comment.user_id = request.user.id 
        comment.article_id = article_id

        comment.save()

        return redirect('articles:detail', id=article_id)
```

## 18. Comment Read

```html
<!-- articles/templates/'detail.html' -->

{% for comment in article.comment_set.all %}
<!-- all은 함수지만 html에서는 () 쓰지 않음 -->
    <li>{{comment.user.username}} : {{comment.content}}</li>
    <!-- 원래 username을 적어야 하는데 user에서 편의성 기능으로 id를 출력해줌 -->
{% endfor %}
```

## 19. Comment Delete
- delete 버튼
```html
<!-- articles/templates/'detail.html' -->
<a href="{% url 'articles:comment_delete' article.id comment.id %}">delete</a>
```
- url
```python
# articles/'urls.py'
path('<int:article_id>/comments/<int:comment_id>/delete', views.comment_delete, name='comment_delete')
```
- def
```python
# artilces/'views.py'
from .models import Comment

def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()

    return redirect('articles:detail', id=article_id)
```
- 문제점: 남이 작성한 댓글까지 삭제할 수 있음 -> 댓글작성자만 댓글삭제 버튼을 볼 수 있게 변경
```html
<!-- articles/templates/'detail.html' -->
{% if user == comment.user %}
    <a href="{% url 'articles:comment_delete' article.id comment.id %}">🐳</a>
{% endif %}
```
- 로그인한 사람만 댓글을 지울 수 있도록 변경
```python
# articles/'views.py'
@login_required
def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()

    return redirect('articles:detail', id=article_id)
    # if문을 통과하지 못하면 바로 return으로 이동
```

# 게시물 기능

## 20. Article Delete
- 로그인한 사용자와 게시글 작성자가 같을 때만 삭제 버튼을 볼 수 있고, 지울 수 있는 기능 추가
```html
<!-- articles/templates/'detail.html' -->
{% if user == article.user %}
    <a href="{% url 'articles:delete' article.id %}">delete</a>
{% endif %}
```
```python
# articles/'urls.py'
path('<int:id>/delete/', views.delete, name='delete')
```
```python
# articles/'views.py'
@login_required
def delete(request, id):
    article = Article.objects.get(id=id)
    if request.user == article.user:
        article.delete()
    
    return redirect('articles:index')
```

## 21. Article Update
```html
<!-- articles/templates/'detail.html' -->
<a href="{% url 'articles:update' article.id %}">update</a>
```
```python
# articles/'urls.py'
path('<int:id>/update/', views.update, name='update')
```
- 기존 정보 출력
```python
# articles/'views.py'
@login_required
def update(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        pass 
    else:
        form = ArticleForm(instance=article)
    context = {
        'form': form,
    }

    return render(request, 'update.html', context)
```
```html
<!-- articles/templates/'update.html' -->
 <form action="" method="POST">
    {% csrf_token %}
    {{form}}
    <input type="submit">
</form>
```
- 저장
```python
# articles/'iews.py'
if request.method == 'POST':
    form = ArticleForm(request.POST, instance=article)
    if form.is_valid():
        form.save()
        return redirect('articles:detail', id=id)
```
- 다른 사람이 작성한 게시글을 수정하지 못하도록 코드 수정
```python
# articles/'views.py'
if request.user != article.user:
# 현재 로그인한 사람 != 게시물을 작성한 사람
    return redirect('articles:index')
```

# bootstrap 편하게 쓰기

## 22. bootstrap v5
- [부트스트랩 라이브러리 v5](https://django-bootstrap-v5.readthedocs.io/en/latest/templatetags.html)
- [부트스트랩 라이브러리 5](https://django-bootstrap5.readthedocs.io/en/latest/templatetags.html)

```shell
pip install django-bootstrap-v5
pip install django-bootstrap
```
- 장고 4버전에서 호환이 되기 때문에 우리가 깔았던 5버전을 삭제하고 4버전을 재다운함

```python
# auth/'settings.py'
INSTALLED_APPS = ['bootstrap5']
```
```html
<!-- extends 아래에 써야함 -->
{% load bootstrap5 %}

{% bootstrap_form form %}
```

# 프로필 기능

## 23. user profile

```html
<!-- ../templates/'base.html' -->
<a href="{% url 'accounts:profile' user.username %}" class="nav-link">{{user}}</a>
```
```python
# accounts/'urls.py'
path('<username>/', views.profile, name='profile')

```
```python
# accounts/'views.py'
def profile(request, username):
    user_profile = User.objects.get(username=username)
    # user와 충돌이 일어날 수 있으므로 이름 변경

    context = {
        'user_profile': user_profile,
        # 'user': request.user # 장고가 우리 모르게 넣어둔 것
    }

    return render(request, 'profile.html', context)
```
```html
<!-- accounts/'profile.html' -->
{% extends 'base.html' %}

{% block body %}
    <h1>{{user_profile.username}}</h1>

    {% for article in user_profile.article_set.all %}
        <li>{{article.title}}</li>
    {% endfor %}
{% endblock %}
```