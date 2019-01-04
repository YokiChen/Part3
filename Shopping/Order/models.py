from django.db import models
from tinymce.models import HTMLField
from User.models import Users
from Goods.models import Goods_mes


# Create your models here.
# 创建类管理器
class OrderManager(models.Manager):
    pass


# 创建订单表
class Orders(models.Model):
    ord_id = models.AutoField(primary_key=True)
    ord_good_num = models.IntegerField()
    ord_good_price = models.IntegerField()
    ord_user_addr = models.CharField(max_length=50)
    # 用户id
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    # 商品id
    good_id = models.ForeignKey(Goods_mes, on_delete=models.CASCADE)

    # 订单管理器
    ordermanager = OrderManager()
    def __str__(self):
        return self.ord_id