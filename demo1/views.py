# views.py
# 说明：Django 视图函数集合（demo1 应用）。
#       本文件包含登录/登出、文章增删改查、搜索、注册等基本视图逻辑。

from django.shortcuts import render, redirect
from django.template.defaultfilters import title

# 导入模型（UserInfo、Article、Category）
from demo1.models import UserInfo
from demo1.models import Article
from demo1.models import Category
from django.http import HttpResponse


# 另一种导入方式（同上）
from .models import Article, UserInfo, Category  
import logging
from django.contrib.auth import logout


# 日志记录器，用于记录服务器端日志（debug/错误等）
logger = logging.getLogger(__name__)

# -------------------------
# 登录与会话相关视图
# -------------------------
def login(request):
    """
    渲染登录页面。仅负责返回 login.html 模板。
    输入：HttpRequest
    输出：render 的 HttpResponse（login.html）
    备注：若已登录逻辑（如直接跳转）在此未实现，由 doLogin 处理会话写入。
    """
    return render(request, 'login.html')


def doLogin(request):
    """
    处理登录请求（POST）。
    - 仅接受 POST 请求，非 POST 将重定向到登录页。
    - 从表单获取 uname 和 upass，与 UserInfo 表匹配。
    - 登录成功：写入 session（username, id），跳转到 'main' 页面。
    - 登录失败：重新渲染 login.html 并带 error_message 提示。

    可以完善的地方：
    - 密码以明文在数据库中比对（userpass）；生产环境应使用加密哈希（例如 Django auth 的密码哈希）。
    - 使用了 UserInfo.objects.filter(...)：可能返回多个用户（如果数据不唯一），此处取第一个。
    - session 写入后跳转到主页面（main）；未对用户活跃状态或权限做校验。
    """
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
    """
    简单的页面访问权限示例：
    - 若 session 中存在 'username'，渲染 hello.html；
    - 否则返回登录页面。
    - 这是基于 session 的访问控制示例，实际项目中应有更完善的认证与权限体系。
    """
    if request.session.has_key('username'):
        return render(request, 'hello.html')
    else:
        return render(request, 'login.html')


# -------------------------
# 文章相关视图：新增、编辑、删除、列表、详情、搜索
# -------------------------
def add(request):
    """
    渲染新增文章页面，模板需要 categories 列表用于选择文章分类。
    返回 add.html 模板并传入 categories。
    """
    categories = Category.objects.all()  # 获取所有类别
    return render(request, 'add.html', {'categories': categories})


def doAdd(request):
    """
    处理新增文章的 POST 表单提交：
    - 从 request.POST 中读取 title, content, c_id，并从 session 中读取用户 id（u_id）。
    - 使用 Article.objects.create(**dicts) 创建文章记录。
    - 完成后重定向到 'main' 页面（文章列表）。

    可以完善的地方：
    - 没有对表单字段做严格校验（如空值、长度限制等）。
    - session['id'] 直接用于数据库字段 u_id，确保 session 可用性和安全性。
    """
    title = request.POST['title']
    content = request.POST['content']
    c_id = request.POST['c_id']
    u_id = request.session['id']
    dicts = {'title': title, 'content': content, 'c_id': c_id, 'u_id': u_id}
    Article.objects.create(**dicts)

    # 添加文章后，重定向到主界面
    return redirect('main')


def edit_article(request, article_id):
    """
    渲染编辑文章页面或处理编辑提交：
    - GET 请求：渲染 edit.html，模板需要 article 与 categories。
    - POST 请求：更新 article 的 title、content、c_id，并保存；然后重定向到 'main'。
    可以完善的地方：没有对用户权限（是否为作者）进行校验，实际应用中应加权限检查。
    """
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
    """
    处理编辑操作（独立函数形式）：
    - 接收 POST 数据并更新指定 article 的 title、content、c_id。
    - 保存并重定向到 'main'。

    注：当前代码和 edit_article 的 POST 分支功能重复，可考虑合并，暂时保持现状不改动。
    """
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
    """
    渲染文章列表（main.html）：
    - 查询所有 Article，循环为每篇文章追加 author_name 与 category_name 属性（用于模板渲染）。
    - 从 session 获取当前用户名用于页面显示（默认为 '未登录用户'）。

    可以改善的地方：
    - 这种写法每个文章会执行两次单条查询（UserInfo.objects.get / Category.objects.get），存在 N+1 查询问题。
    - 或许可以使用 select_related / prefetch_related 或在模型中建立外键，
      减少数据库查询次数和提高性能。
    """
    articles = Article.objects.all()
    for article in articles:
        article.author_name = UserInfo.objects.get(id=article.u_id).username
        article.category_name = Category.objects.get(id=article.c_id).name

    username = request.session.get('username', '未登录用户')
    return render(request, 'main.html', {'articles': articles, 'username': username})


def delete_article(request, article_id):
    """
    处理删除文章：
    - 仅接受 POST 请求进行删除操作（页面上应通过表单 POST 调用此视图）。
    - 先检查 session 中是否有 'id'（是否已登录），若未登录则重定向到登录页。
    - 尝试删除指定文章，若不存在则直接重定向到主页面。
    - 检查当前用户是否有权限删除该文章（例如是否为文章作者）。这一功能其实已经实现，但后续或许该重构一下。
    """
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
    """
    渲染文章详情页面：
    - 查询指定文章，获取作者与分类（使用 filter().first() 防止抛异常）。
    - 为 article 动态添加 author_name 与 category_name 属性供模板渲染。
    """
    article = Article.objects.get(id=article_id)

    # 查询并添加作者名和类别名
    author = UserInfo.objects.filter(id=article.u_id).first()
    category = Category.objects.filter(id=article.c_id).first()
    article.author_name = author.username if author else "未知作者"
    article.category_name = category.name if category else "未知类别"

    return render(request, 'article_detail.html', {'article': article})


def search(request):
    """
    搜索文章：
    - 从 GET 参数获取 q（查询关键字）。
    - 若有关键词，使用 title__icontains 或 content__icontains 做模糊查询（取并集）。
    - 为每篇结果文章补充 author_name 与 category_name 字段，最后渲染 search.html。

    可以改善的地方
    - 目前使用了两个 QuerySet 的按位或（|），在大数据量下可能效率不高。
    - 可考虑对全文检索使用专门工具（如 Elasticsearch）或使用 Django 的全文检索功能。
    """
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


# -------------------------
# 用户注册与登出
# -------------------------
def register(request):
    """
    处理用户注册：
    - POST 请求：读取 username、password、confirm_password，并检查密码一致性。
    - 如果两次密码不一致，返回 register.html 并带 message 提示；
    - 否则在 UserInfo 表创建新用户并跳转到登录页面（带成功 message）。

    可以改善的地方：
    - 当前将密码以明文存储到 UserInfo.userpass 字段；生产环境建议使用 Django 自带的用户模型与密码哈希。
    - 需注意用户名唯一性校验（当前未检测重复用户名），可在创建前检查是否已存在。
    """
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
    """
    注销（登出）视图：
    - 使用 django.contrib.auth.logout 清理认证相关 session（如果使用 Django auth）。
    - 之后重定向到登录页面。

    可以改善的地方：
    - 这里调用 logout 若没有使用 Django 内置认证系统仅会清理 auth 相关 session；
      若需要清理自定义 session（如 'username','id'），可额外调用 request.session.flush() 或 pop 对应键。
    """
    logout(request)
    return redirect('login')  # 重定向到登录页面
