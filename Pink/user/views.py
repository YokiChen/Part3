from django.shortcuts import render,reverse
from . import models

from . import utils
from io import BytesIO

from django.core.cache import cache

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

# 分页
from django.core.paginator import Paginator
from django.conf import settings
a=settings.PAGESIZE


# Create your views here.

def index(req):
    # return HttpResponse("hhhhhh")
    return render(req, 'html_lib/index.html')


def blog_login(req):
    if req.method=='GET':
        return render(req, 'html_lib/blog_login.html')
    elif req.method == 'POST':
        print(req.POST)
        username = req.POST['name']
        userpwd = req.POST['password']
        code=req.POST['code']
        print(code)
        # 获取所有学生的信息
        u = models.student.addStu.all()
        for i in u:
            if username == i.name:
                if userpwd == i.password:
                    if req.session['check_code'] != code:
                        print(req.session['check_code'])
                        return render(req, 'html_lib/blog_loginsuccess.html',{'error':'faultcode'})
                    else:
                        print("登录成功")
                        req.session['loginUser'] = i
                        print(req.session['loginUser'].name)
                        return HttpResponse(render(req, 'html_lib/blog_loginsuccess.html'))
                else:
                    print("密码错误")
                    return HttpResponse(render(req, 'html_lib/blog_loginsuccess.html', {'error': 'nopwd'}))

        print("用户不存在")
        return HttpResponse(render(req, 'html_lib/blog_loginsuccess.html', {'error': 'noname'}))


def pink_base(req):
    return render(req, 'pink_base.html')


# 注册页面的实现
def blog_regists(req):
    print(req.session['loginUser'])
    if req.method == 'GET':
        return render(req,'html_lib/blog_regist.html')
    elif req.method == 'POST':
        name = req.POST['name']
        # 输入框里输入的密码
        pwd = req.POST['pwd']
        pwdd = req.POST['pwdd']
        teaid_id = req.POST['teaid_id']
        header = req.FILES.get(str('header'))
        # 查询所有已注册用户的信息
        oldUser = models.student.addStu.all()
        print(oldUser)
        for user in oldUser:
            print(user)
            if user.name!= name:
                if pwd != pwdd:
                    return render(req, 'html_lib/blog_registsuccess.html',{'errorRe': '密码两次输入不同，请重新输入'})
                else:
                    if len(pwd) < 6:
                        print('哈哈')
                        return render(req, 'html_lib/blog_registsuccess.html', {'errorRe': '密码长度不足'})
                    else:
                        stu = models.student(name=name, password=pwd, teaid_id=teaid_id, header=header)
                        stu.save()
                        return render(req, 'html_lib/blog_registsuccess.html')
            else:
                return render(req, 'html_lib/blog_registsuccess.html',{'errorRe':'用户名已存在'})



def teacher(req):
    teachers=models.Teacher.useaddTea.all()
    return render(req,'html_lib/alltea.html',{'teachers':teachers})


def student(req):
    # 设置显示每页条数
    students=models.student.addStu.all()
    pagenum = req.GET.get('pagenum',default=1)
    pagena=Paginator(students,a)
    # 点击查看当前页内容
    page = pagena.page(int(pagenum))
    print(page)
    return render(req,'html_lib/allstu.html',{'pagena':pagena,'page':page})


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
    # artcles=cache.get('arts')
    # if artcles is None:
    #     artcles=models.Article.addArt.all()
    #     cache.set('artcles',artcles)
    #     print('放入缓存成功')
    # artcles=models.Article.addArt.filter()
    artcles = models.Article.addArt.all()
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


# @login_required(login_url='user: login')
def updateart(req,pp):
    if req.method == 'GET':
        # # id=req.GET
        id = req.GET.get('aid')
        art=models.Article.addArt.get(id=pp)
        return render(req,'html_lib/updateart.html',{'art':art})
    elif req.method == 'POST':
        # 指定id进行修改
        aid=req.POST['aid']
        title = req.POST['title']
        content= req.POST['content']
        art=models.Article.addArt.get(pk=pp)
        print(aid,title,content)
        art.author = title
        art.content = content
        art.save()
        return HttpResponse(Artcle(req))

# @login_required(login_url='user: login')
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


def logoff(req):
    return render(req,'html_lib/logoff.html')


def login1(req):
    return render(req,'html_lib/login1.html')

def register1(req):
    return render(req,'html_lib/register1.html')

def regis(request):
    return render(request, 'html_lib/register1.html')

























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

# from . import Forms


# @csrf_exempt
# def userform(req):
#     form=Forms.userForm()
#     if req.method == 'GET':
#         return render(req, 'html_lib/userForm1.html',{'form':form})
#     elif req.method == 'POST':
#         form = Forms.userForm(req.POST)
#         print(form.data)
#         return render(req, 'html_lib/form_text.html')





