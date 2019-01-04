from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^index/$', views.index),
    # url(r'^search', views., name='createCode'),


    url(r'^blog_login/$', views.blog_login,name='login'),
    url(r'^pink_base/$', views.pink_base),
    # url(r'^blog_loginsuccess/$',views.blog_loginsuccess),
    # url(r'^blog_regist/$', views.blog_regist),
    # url(r'^blog_registsuccess/$', views.blog_registsuccess),
    url(r'^blog_regist/$', views.blog_regists),

    url(r'^allteacher/$', views.teacher, name='alltea'),
    url(r'^allstu/', views.student, name='allstu'),
    url(r'^updateUser/(?P<xx>\w+)/$', views.updateUser, name='updateUser'),
    url(r'^deleteUser/(?P<xx>\w+)/$', views.deleteUser, name='deleteUser'),
    url(r'^putartcle/(?P<xx>\w+)/$', views.putartcle, name='putartcle'),
    url(r'^allart/$', views.Artcle, name='allart'),
    url(r'^blog_end/$', views.logoff),
    url(r'^updateart/(?P<id>\w+)/$', views.updateart, name='updateart'),
    url(r'^deleteart/(?P<id>\w+)/$', views.deleteUser, name='deleteart'),
    url(r'^creatCode', views.create_code_img, name='createCode'),




]