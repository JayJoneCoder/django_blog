from django.db import models

# Create your models here.

class UserInfo(models.Model):
    id=models.AutoField(primary_key=True,auto_created=True)
    username=models.CharField(max_length=50)
    userpass=models.CharField(max_length=50)

class Category(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    name=models.CharField(max_length=50)

class Article(models.Model):
    id=models.IntegerField(primary_key=True,auto_created=True)
    title=models.CharField(max_length=50)
    content=models.TextField()
    create_time=models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    c_id=models.IntegerField()
    u_id = models.IntegerField()


