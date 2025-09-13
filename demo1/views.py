from django.shortcuts import render, redirect
from django.template.defaultfilters import title

from demo1.models import UserInfo
from demo1.models import Article
from demo1.models import Category
from django.http import HttpResponse


from .models import Article, UserInfo, Category  # 确保引入你的模型
# Create your views here.
import logging
from django.contrib.auth import logout


logger = logging.getLogger(__name__)
def login(request):
    return render(request, 'login.html')

def doLogin(request):
    if request.method != 'POST':
        return redirect('login')

    username = request.POST.get('uname', '').strip()
    password = request.POST.get('upass', '')

    users = UserInfo.objects.filter(username=username, userpass=password)
    if users.exists():
        user = users.first()
        # 写 session
        request.session['username'] = user.username
        request.session['id'] = user.id
        return redirect('main')
    else:
        # 登录失败，显示错误
        return render(request, 'login.html', {'error_message': '用户名或密码错误'})

def hello(request):
    if request.session.has_key('username'):
        return render(request, 'hello.html')
    else:
        return render(request, 'login.html')


def add(request):
    categories = Category.objects.all()  # 获取所有类别
    return render(request, 'add.html', {'categories': categories})



def doAdd(request):
    title = request.POST['title']
    content = request.POST['content']
    c_id = request.POST['c_id']
    u_id = request.session['id']
    dicts = {'title': title, 'content': content, 'c_id': c_id, 'u_id': u_id}
    Article.objects.create(**dicts)

    # 添加文章后，重定向到主界面
    return redirect('main')



def edit_article(request, article_id):
    article = Article.objects.get(id=article_id)
    categories = Category.objects.all()  # 获取所有类别
    if request.method == "POST":
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.c_id = request.POST['c_id']
        article.save()
        return redirect('main')
    return render(request, 'edit.html', {'article': article, 'categories': categories})

def doEdit(request, article_id):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        c_id = request.POST['c_id']

        # 获取要编辑的文章
        article = Article.objects.get(id=article_id)

        # 只更新标题、内容和分类ID，不更新 create_time
        article.title = title
        article.content = content
        article.c_id = c_id

        # 保存文章，Django自动处理 create_time 字段
        article.save()

        # 编辑完成后重定向到文章列表或其它页面
        return redirect('main')


def article_list(request):
    articles = Article.objects.all()
    for article in articles:
        article.author_name = UserInfo.objects.get(id=article.u_id).username
        article.category_name = Category.objects.get(id=article.c_id).name

    username = request.session.get('username', '未登录用户')
    return render(request, 'main.html', {'articles': articles, 'username': username})


def delete_article(request, article_id):
    # 检查用户是否已登录
    if 'id' not in request.session:
        return redirect('login')

    if request.method == "POST":
        try:
            article = Article.objects.get(id=article_id)
            article.delete()
            return redirect('main')  # 确保这里是重定向到文章列表
        except Article.DoesNotExist:
            return redirect('main')  # 如果文章不存在，重定向到列表页
    return redirect('main')  # 如果不是 POST 请求，重定向到列表页

def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)

    # 查询并添加作者名和类别名
    author = UserInfo.objects.filter(id=article.u_id).first()
    category = Category.objects.filter(id=article.c_id).first()
    article.author_name = author.username if author else "未知作者"
    article.category_name = category.name if category else "未知类别"

    return render(request, 'article_detail.html', {'article': article})


def search(request):
    query = request.GET.get('q')
    if query:
        articles = Article.objects.filter(title__icontains=query) | Article.objects.filter(content__icontains=query)
    else:
        articles = Article.objects.all()

    for article in articles:
        author = UserInfo.objects.filter(id=article.u_id).first()
        category = Category.objects.filter(id=article.c_id).first()
        article.author_name = author.username if author else "未知作者"
        article.category_name = category.name if category else "未知类别"

    return render(request, 'search.html', {'articles': articles, 'query': query})


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'message': '两次输入的密码不一致，请重新输入。'})

        UserInfo.objects.create(username=username, userpass=password)
        return render(request, 'login.html', {'message': '注册成功，请登录。'})
    return render(request, 'register.html')



def logout_view(request):
    logout(request)
    return redirect('login')  # 重定向到登录页面
