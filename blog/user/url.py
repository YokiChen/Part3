from django.conf.urls import url

from . import views


urlpatterns = [
    # 新博客
    url(r'^index/$', views.index),
    url(r'^index_son/$', views.index_son),
    url(r'^index_son/$', views.index_son),
    url(r'^blog_login/$', views.blog_login),
    url(r'^blog_loginsuccess/$', views.blog_loginsuccess),
    url(r'^blog_regist/$', views.blog_regist),
    url(r'^blog_registsuccess/$', views.blog_registsuccess),

    url(r'^allteacher/$', views.teacher,name='alltea'),
    url(r'^allstudent/$', views.student,name='allstu'),
    url(r'^updateUser/(?P<xx>\w+)/$',views.updateUser,name='updateUser'),
    url(r'^deleteUser/(?P<xx>\w+)/$',views.deleteUser,name='deleteUser'),
    url(r'^putartcle/(?P<xx>\w+)/$',views.putartcle,name='putartcle'),
    url(r'^allart/$', views.Artcle),
    url(r'^updateart/(?P<id>\w+)/$', views.updateart,name='updateart'),
    url(r'^deleteart/(?P<id>\w+)/$',views.deleteUser,name='deleteart'),
    url(r'^creatCode',views.create_code_img,name='createCode'),


    url(r'^ajaxa/$',views.text_ajax ),
    url(r'^userartcle/$',views.userartcle),
    url(r'^reg/$', views.reg),
    url(r'^userform/$',views.userform),
    url(r'^form_text/$', views.userform),



]