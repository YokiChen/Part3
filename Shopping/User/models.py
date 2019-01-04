from django.db import models
from tinymce.models import HTMLField

# Create your models here.

# 创建管理器


# 创建用户管理器
class UserManager(models.Manager):
    pass


# 创建地址表管理器
class RecManager(models.Manager):
    pass


# 创建表

# 用户表
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=20)
    user_pwd = models.CharField(max_length=20)
    user_age = models.IntegerField()
    user_header = models.ImageField(upload_to='static/img/user_header/',null=True,default='static/user/user1.jpg')
    user_sex = models.CharField(max_length=5)
    user_phone = models.CharField(max_length=14)
    # 用户管理器
    usermanage = UserManager()

    def __str__(self):
        return self.user_name


# 收货地址表
class Rec(models.Model):
    # 收货地址id
    add_id = models.AutoField(primary_key=True)
    # 收货人姓名
    rec_name = models.CharField(max_length=20)
    rec_phone = models.CharField(max_length=20)
    rec_country = models.CharField(max_length=15)
    rec_pro = models.CharField(max_length=20)
    rec_city = models.CharField(max_length=10)
    rec_area = models.CharField(max_length=20)
    rec_deta = models.CharField(max_length=40)
    # 地址管理器
    recmanage = RecManager()
    #外键
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.rec_name