from django.conf.urls import url
from . import views


urlpatterns = [
    url('^storeIndex/$', views.storeIndex, name='storeIndex'),
    url('^Shopowner/$', views.Shopowner, name='Shopowner'),
    url('^SellerLogin/$', views.SellerLogin, name='SellerLogin'),
    url('^StoreReg/$', views.StoreReg, name='StoreReg'),
    url('^allStore/$', views.allStore, name='allStore'),
    url('^onestore/(?P<store_id>\d+)/$', views.onestore, name='onestore'),
    url('^uploadGoods/(?P<store_id>\d+)/$', views.uploadGoods, name='uploadGoods'),
    url('^updateGoods/(?P<store_id>\d+)/(?P<good_id>\d+)/$', views.updateGoods, name='updateGoods'),
    url('^s_allGoods/(?P<store_id>\d+)/$', views.s_allGoods, name='s_allGoods'),
    url('^undercarriage/(?P<store_id>\d+)/(?P<good_id>\d+)/$', views.undercarriage, name='undercarriage'),
    url('^exitSeller/$', views.exitSeller, name='exitSeller'),
]