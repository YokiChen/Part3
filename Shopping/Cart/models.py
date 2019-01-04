from django.db import models
from User.models import Users
from Goods.models import Goods_mes
from Store.models import Stores

# Create your models here.
class CartManager(models.Manager):
    pass


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    cart_good_num = models.IntegerField()
    cart_single = models.IntegerField()
    # 外键
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    good_id = models.ForeignKey(Goods_mes, on_delete=models.CASCADE)
    store_id = models.ForeignKey(Stores, on_delete=models.CASCADE)
    # 购物车的管理器
    cartmanager = CartManager()

    def __str__(self):
        return self.cart_id