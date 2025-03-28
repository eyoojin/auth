from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:index')

    else:
        form = ArticleForm()
    
    context = {
        'form': form,
    }

    return render(request, 'create.html', context)

def detail(request, id):
    article = Article.objects.get(id=id)
    form = CommentForm()

    context = {
        'article': article,
        'form': form,
    }

    return render(request, 'detail.html', context)

@login_required
def comment_create(request, article_id):
    # if request.method == 'POST':
    #     pass
    # else:
    #     pass
    # 댓글 작성에는 get요청이 들어오지 않기 때문에 if문 안쪽의 코드만 있으면 됨
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)

        # 객체를 저장하는 경우
        # comment.user = request.user # 유저 정보 = 현재 로그인한 사람
        # article = Article.objects.get(id=article_id) # 게시물 정보 = 현재 게시글
        # comment.article = article

        # id 값을 저장하는 경우
        # DB에 저장되는 숫자
        comment.user_id = request.user.id 
        comment.article_id = article_id

        comment.save()

        return redirect('articles:detail', id=article_id)

@login_required
def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()

    return redirect('articles:detail', id=article_id)