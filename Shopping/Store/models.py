from django.db import models
from tinymce.models import HTMLField
from Goods.models import Goods_mes

# Create your models here.
class StoreManager(models.Manager):
    pass
class SellerManager(models.Manager):
    pass
class Goods_infoManager(models.Manager):
    pass


# 店主信息表
class Seller(models.Model):
    seller_id = models.AutoField(primary_key=True)
    seller_account = models.CharField(max_length=20)
    seller_name = models.CharField(max_length=10)
    seller_phone = models.CharField(max_length=11)
    seller_pwd = models.CharField(max_length=16)
    seller_header = models.ImageField(upload_to='static/img/Storeimg/seller/',null=True)
    sellermanager = SellerManager()


# 创建店铺表
class Stores(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=20)
    store_pic = models.ImageField(upload_to='static/img/Storeimg/img/', null=True)
    store_deta = HTMLField()
    # 店主id
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE)
    storemanage = SellerManager()

    def __str__(self):
        return self.store_name


# 店铺商品表
class Goods_info(models.Model):
    good_info_id = models.AutoField(primary_key=True)
    sale_num = models.IntegerField()
    rema_num = models.IntegerField()
    # 外键
    store_id = models.ForeignKey(Stores, on_delete=models.CASCADE)
    good_id = models.ForeignKey(Goods_mes, on_delete=models.CASCADE)
    goodinfo = Goods_infoManager()
