# Django 博客项目

一个基于 Django 的个人博客系统，支持文章管理、用户注册登录、文章搜索与分类功能，并遵循开源协议发布。

---

## 功能特性

- 用户注册、登录、注销功能
- 文章发布、编辑、删除
- 按类别分类和全文搜索文章
- 简洁响应式前端界面，支持不同设备访问
- 项目开源，遵循 GPLv3 许可

---

## 技术栈

- Python 3.x
- Django 4.x
- SQLite（默认开发数据库，可替换为 PostgreSQL/MySQL）
- HTML、CSS、Bootstrap 4

---

## 安装与运行

克隆仓库：
```bash
git clone https://github.com/JayJoneCoder/django_blog.git
```
进入项目目录：
```
cd django_blog
```
创建虚拟环境并激活：
```
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```
安装django：
```
pip install django
```
迁移数据库：
```
python manage.py migrate
```
运行开发服务器：
```
python manage.py runserver
```
打开浏览器访问：
```
http://127.0.0.1:8000/
```
输入帐号密码：
可以自行注册。如果将数据库也一并保存了的话，可以用已有的数据，比如帐号：zhangsan 密码：12345

---

## 部分页面的演示图片

### 登录页面
<img width="2559" height="1449" alt="图片" src="https://github.com/user-attachments/assets/3b5c913e-3d18-480f-b5f2-ca3e9340b885" />

### 文章列表页面
<img width="2556" height="1430" alt="图片" src="https://github.com/user-attachments/assets/e3a8a4f5-f7a1-4b60-87e2-d347306ad96d" />

### 搜索结果页面
<img width="2559" height="1447" alt="图片" src="https://github.com/user-attachments/assets/5cacb6de-8d24-4537-b508-40878d275b98" />

---

## License

本项目采用 GPLv3开源许可。
欢迎批评、指正、学习与贡献。
