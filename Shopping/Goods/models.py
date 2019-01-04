from django.db import models
from tinymce.models import HTMLField

# Create your models here.


# 创建商品的类管理器
class GoodMesManager(models.Manager):
    pass

class GoodkingManager(models.Manager):
    pass


# 创建商品信息表
class Goods_mes(models.Model):
    good_id = models.AutoField(primary_key=True)
    good_name = models.CharField(max_length=15)
    good_price = models.IntegerField()
    good_inst = HTMLField()
    good_img = models.ImageField(upload_to='static/img/Goodsimg/Goods/',null=True)

    # 管理器
    goodmesmanage = GoodMesManager()

    def __str__(self):
        return self.good_name

# 创建商品类型表
class Good_kind(models.Model):
    kind_id = models.AutoField(primary_key=True)
    first = models.CharField(max_length=4)
    second = models.CharField(max_length=8)
    third = models.CharField(max_length=12)
    active1 = models.CharField(max_length=8)
    active2 = models.CharField(max_length=8)

    #外键
    good_id = models.ForeignKey(Goods_mes, on_delete=models.CASCADE)

    # 管理器
    goodkingmanager = GoodkingManager()

    def __str__(self):
        return self.kind_id



