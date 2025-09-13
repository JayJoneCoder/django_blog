"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from demo1 import views
urlpatterns = [
    #path("admin/", admin.site.urls),
    path('', views.login, name='login'),  # 登录页面
    path('doLogin', views.doLogin, name='doLogin'),  # 处理登录
    path('add.html', views.add, name='add'),  # 添加文章页面
    path('doAdd', views.doAdd, name='doAdd'),  # 处理添加文章
    path('edit/<int:article_id>/', views.edit_article, name='edit_article'),  # 编辑文章
    path('doEdit/<int:article_id>/', views.doEdit, name='doEdit_article'),  # 处理编辑
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),  # 删除文章
    path('main/', views.article_list, name='main'),  # 文章列表
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('search/', views.search, name='search'),  # 搜索结果页面
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),



]


