from django.conf.urls import url
from . import views


urlpatterns = [
    url('^index/$', views.index, name='index'),
    url('^createimg/$', views.createimg, name='createimg'),
    url('^userLogin/$', views.userLogin, name='userlogin'),
    url('^userRegister/$', views.userRegister, name='userregister'),
    url('^updateUser/$', views.updateUser, name='updateUser'),
    url('^addrs/$', views.addrs, name='addrs'),
    url('^addAddr/$', views.addAddr, name='addAddr'),
    # url('^userloginss/$', views.exitUser, name='userloginss'),
	url('^u_allgoods/$',views.allGoods,name='u_allgoods'),
    url('^updatePwd/$', views.updatePwd, name='updatePwd'),


    # url('^allGoods/$', views.allGoods, name='allGoods'),
    url('^buyGoods/(?P<good_id>\d+)/(?P<store_id>\d+)/$', views.buyGoods, name='buyGoods'),
    url('^createOrder/(?P<good_id>\d+)/(?P<store_id>\d+)/$', views.createOrder, name='createOrder'),
    url('^lookOrder/$', views.lookOrder, name='lookOrder'),
    url('^exitUser/$', views.exitUser, name='exitUser'),
	url('^enterShop/(?P<store_id>\d+)/$', views.enterShop, name='enterShop'),
    url('^addCart/(?P<good_id>\d+)/(?P<store_id>\d+)/$', views.addCart, name='addCart'),


	url('^searchGoods/$', views.searchGoods, name='searchGoods'),
    # 关于订单的
    url('^createOrder/(?P<good_id>\d+)/(?P<store_id>\d+)/$', views.createOrder, name='createOrder'),
    # 关于购物车的
    url('^addCart/(?P<good_id>\d+)/(?P<store_id>\d+)/$', views.addCart, name='addCart'),
    url('^lookCart/$', views.lookCart, name='lookCart'),
    url('^delCart/(?P<c_id>\d+)/$', views.delCart, name='delCart'),
    url('^cartOrder/$', views.cartOrder, name='cartOrder'),
    url('^prodectOrder/$', views.prodectOrder, name='prodectOrder'),
    url('^postOrder/(?P<good_id>\d+)/(?P<store_id>\d+)/$', views.postOrder, name='postOrder'),
    # 商品详情页
    url('^goodDetal/(?P<good_id>\d+)/(?P<store_id>\d+)/$', views.goodDetal, name='goodDetal'),
]