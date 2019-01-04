from django.shortcuts import render
from . import models

from io import BytesIO
from . import utils

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

# Create your views here.

def index(req):
    return HttpResponse (render(req,'index.html'))


# 父模板
def baseblog(req):
    return HttpResponse (render(req,'baseblog.html'))


# 儿子模板
def index_son(req):
    return HttpResponse (render(req,'html_lib/index_son.html'))


# 登录
def blog_login(req):
    return HttpResponse (render(req,'html_lib/blog_login.html'))


# 登录成功
@csrf_exempt
def blog_loginsuccess(req):
    Info=req.POST
    username=Info['name']
    userpwd=Info['password']
    # 获取所有学生的信息
    u=models.student.addStu.all()
    for i in u:
        if username == i.name:
            if userpwd == i.password:
                print("登录成功")
                return HttpResponse (render(req,'html_lib/blog_loginsuccess.html'))
            else:
                print("密码错误")
                return HttpResponse(render(req, 'html_lib/blog_loginsuccess.html',{'error':'nopwd'}))

        print("用户不存在")
    return HttpResponse (render(req,'html_lib/blog_loginsuccess.html',{'error':'noname'}))


# 注册
def blog_regist(req):
    return HttpResponse (render(req,'html_lib/blog_regist.html'))
# 注册成功


def blog_registsuccess(req):
    name=req.POST['name']
    # 输入框里输入的密码
    pwd=req.POST['pwd']
    pwdd=req.POST['pwdd']
    teaid_id=req.POST['teaid_id']
    # 查询所有已注册用户的信息
    oldUser=models.student.addStu.all()
    for oldu in oldUser:
        if oldu == name:
            return HttpResponse(render(req, 'html_lib/blog_registsuccess.html', {'errorRe':'用户名已存在'}))
        else:
            if pwd != pwdd:
                return HttpResponse(render(req, 'html_lib/blog_registsuccess.html',{'errorRe':'密码两次输入不同，请重新输入'}))
            else:
                if len(pwd)<6:
                    return HttpResponse(render(req, 'html_lib/blog_registsuccess.html',{'errorRe':'密码长度不足'}))
                else:
                    stu=models.student(name=name, password=pwd, teaid_id=teaid_id)
                    stu.save()
                    return HttpResponse(render(req, 'html_lib/blog_registsuccess.html'))


def teacher(req):
    teachers=models.Teacher.useaddTea.all()
    return render(req,'html_lib/alltea.html',{'teachers':teachers})


def student(req):
    students=models.student.addStu.all()
    return render(req,'html_lib/allstu.html',{'students':students})


def updateUser(req,xx):
    if req.method == 'GET':
        # # id=req.GET
        id = req.GET.get('sid')
        user=models.student.addStu.get(id=xx)
        return render(req,'html_lib/updateUser.html',{'user':user})
    elif req.method == 'POST':
        # 指定id进行修改
        sid=req.POST['sid']
        name = req.POST['name']
        password = req.POST['pwd']
        user=models.student.addStu.get(pk=xx)
        print(sid,name,password)
        user.name = name
        user.password = password
        user.save()
        return HttpResponse(student(req))


def deleteUser(req,xx):
    id=req.GET.get('sid')
    user=models.student.addStu.get(pk=xx)
    user.delete()
    return HttpResponse(student(req))


def userartcle(req):
    return HttpResponse(render(req, 'html_lib/putartcle.html'))


def Artcle(req):
    artcles=models.Article.addArt.filter()
    return HttpResponse(render(req, 'html_lib/allart.html' ,{'artcles':artcles} ))

def putartcle(req, xx):
    if req.method == 'GET':
        id = req.GET.get('sid')
        user = models.student.addStu.get(pk=xx)
        return render(req,'html_lib/putartcle.html')
    elif req.method == 'POST':
        user=models.student.addStu.get(pk=xx)
        idd=user.id
        print(req.POST['title'],req.POST['content'])
        title=req.POST['title']
        content=req.POST['content']
        art = models.Article(content=content,author=title,stuid_id=idd)
        art.save()
        # 用户主键是文章列表的外键，筛选出和用户主键和文章列表外键相同的文章
        arts=models.Article.addArt.filter(stuid_id=idd)
        return render(req,'html_lib/allart.html',{'idd':idd,'arts':arts})

# 文章处理
# 修改文章
def updateart(req,id):
    if req.method == 'GET':
        # # id=req.GET
        id = req.GET.get('aid')
        art=models.Article.addArt.get(id=id)
        return  HttpResponse('哈哈哈哈')
        # return render(req,'html_lib/updateart.html',{'art':art})
    elif req.method == 'POST':
        # 指定id进行修改
        aid=req.POST['aid']
        title = req.POST['title']
        content= req.POST['content']
        art=models.Article.addArt.get(pk=id)
        print(aid,title,content)
        art.author = title
        art.content = content
        art.save()
        return HttpResponse(Artcle(req))


def deleteart(req,id):
    id=req.GET.get('aid')
    art=models.Article.addArt.get(pk=id)
    art.delete()
    return HttpResponse(Artcle(req))



# 定义验证码视图处理函数：
def create_code_img(req):
    # 在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img, code = utils.create_code()
    # 保存验证码信息到 session 中，方便下次表单提交时进行验证操作
    req.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())

























@csrf_exempt
def text_ajax(req):
    if req.method == 'GET':
        return  render(req, 'html_lib/text_ajax.html')
    elif req.method== 'POST':
        res={}
        res['data']={'name':'Tony','age':18}
        # user=models.student.addStu.get(pk=1)
        # user=model_to_dict(user)
        # print(user)
        # return JsonResponse(user)

        users=models.student.addStu.all()
        users=serialize('json',users)
        print(users)
        return HttpResponse (users)


from django.db import transaction


@transaction.atomic
def reg(req):
    # 设置 保存点
    sid = transaction.savepoint()
    try:
        user=models.student(name='xiaochilao',password='12345',teaid_id='1' )
        user.save()
        transaction.savepoint_commit(sid)
        return HttpResponse('小姐姐辛苦了，')
    # user在
    except:
        transaction.savepoint_rollback(sid)
        return HttpResponse ('不辛苦不辛苦')


from . import Forms


@csrf_exempt
def userform(req):
    form=Forms.userForm()
    if req.method == 'GET':
        return render(req, 'html_lib/userForm1.html',{'form':form})
    elif req.method == 'POST':
        form = Forms.userForm(req.POST)
        print(form.data)
        return render(req, 'html_lib/form_text.html')



