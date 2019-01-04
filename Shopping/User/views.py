from django.shortcuts import render,HttpResponse,redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
from io import BytesIO

from . import util1
from . import models
from Store.models import Stores,Goods_info
from Goods.models import Good_kind,Goods_mes
from Order.models import Orders
from Cart.models import Cart

# Create your views here.


# 验证码
def createimg(req):
    # 在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img, code = util1.create_code()
    # 保存验证码信息到 session 中，方便下次表单提交时进行验证操作
    req.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


# 首页
def index(req):
    return render(req,'user/index.html')


@csrf_exempt
# 用户登录
def userLogin(req):
    if req.method == 'GET':
        return render(req, 'user/login.html')
    else:
        user_name = req.POST['user_name']
        # user_account = req.POST['user_account']
        user_pwd = req.POST['user_pwd']
        code = req.POST['code']
        print(user_name)
        user = models.Users.usermanage.filter(user_name=user_name)
        if len(user) != 0:
            if user[0].user_pwd == user_pwd:
                if req.session['check_code'] == code:
                    req.session['LoginUser'] = user[0]
                    # return render(req, 'user/Login_index.html')
                    return render(req, 'user/userloginss.html')
                else:
                    str1 = '验证码错误，请重新登录'
                    return render(req, 'user/login.html', {'msg1': str1})
            else:
                str1 = '密码错误'
                return render(req, 'user/login.html', {'msg2': str1})
        else:
            str1 = "用户不存在，请重新登录"
            return render(req, 'user/login.html', {'msg3': str1})


# 装饰器，判断是否登录
def require_login1(fn):
    def inner_fn(req, *args, **keyargs):
        if req.session.has_key('LoginUser'):
            result = fn(req,*args, **keyargs)
            return result
        else:
            return redirect("/user/userLogin/")
    return inner_fn


#用户注册
@csrf_exempt
def userRegister(req):
    if req.method == 'GET':
        return render(req, 'user/register.html')
    else:
        user_name = req.POST['user_name']
        user_age = req.POST['user_age']
        user_sex = req.POST['user_sex']
        user_phone = req.POST['user_phone']
        code = req.POST['code']
        user_pwd = req.POST['user_pwd']
        user_again_pwd = req.POST['user_pwd_again']
        user = models.Users.usermanage.filter(user_name=user_name)
        if req.session['check_code'] == code:
            if len(user) == 0:
                if len(user_pwd)>=8 and len(user_pwd)<=16:
                    if len(user_phone) == 11:
                        if user_pwd == user_again_pwd:
                            try:
                                user_header = req.FILES['user_header']
                                nuser = models.Users(user_name=user_name,user_pwd=user_pwd,user_age=user_age,user_header=user_header,user_sex=user_sex,user_phone=user_phone)
                                nuser.save()
                                return render(req,'user/login.html')
                            except:
                                nuser = models.Users(user_name=user_name, user_pwd=user_pwd, user_age=user_age,
                                                     user_header='null', user_sex=user_sex, user_phone=user_phone)
                                nuser.save()
                                return render(req, 'user/login.html')
                        else:
                            str1 = '两次输入的密码不相同，请重新输入'
                            return render(req, 'user/register.html', {'msg1': str1})
                    else:
                        str1 = '手机号码长度为11位，请重新输入'
                        return render(req, 'user/register.html', {'msg2': str1})
                else:
                    str1 = '规定密码长度为8-16位，请重新输入'
                    return render(req, 'user/register.html', {'msg3': str1})
            else:
                str1 = '用户名已存在，请重新输入'
                return render(req, 'user/register.html', {'msg4': str1})
        else:
            str1 = '验证码错误，请重新输入'
            return render(req, 'user/register.html', {'msg5': str1})



#修改个人信息
@require_login1
@csrf_exempt
def updateUser(req):
    if req.method == 'GET':
        return render(req, 'user/updateUser.html')
    else:
        user_name = req.POST['user_name']
        user_age = req.POST['user_age']
        # user_sex = req.POST['user_sex']
        user_phone = req.POST['user_phone']
        user_header = req.FILES['user_header']
        code = req.POST['code']

        user = models.Users.usermanage.filter(user_name=user_name)
        if req.session['check_code'] == code:
            if len(user) == 0 or len(user)==1 :
                    if len(user_phone) == 11:
                            user_id = req.session['LoginUser'].user_id
                            user1 = models.Users.usermanage.filter(user_id=user_id)

                            uuser = user1.update(user_name=user_name, user_age=user_age,
                                                 user_header=user_header,  user_phone=user_phone)
                            return render(req, 'user/userloginss.html')
                    else:
                        str1 = '手机号码长度为11位，请重新输入'
                        return render(req, 'user/updateUser.html', {'msg2': str1})
            else:
                str1 = '用户名已存在，请重新输入'
                return render(req, 'user/updateUser.html', {'msg4': str1})
        else:
            str1 = '验证码错误，请重新输入'
            return render(req, 'user/updateUser.html', {'msg5': str1})


# 修改密码
def updatePwd(req):
    if req.method == 'GET':
        return render(req, 'user/updatePwd.html' )
    else:
        oldpwd = req.POST['oldpwd']
        newpwd = req.POST['newpwd']
        newpwd1 = req.POST['newpwd1']
        user = req.session['LoginUser']
        user1 = models.Users.usermanage.filter(user_id = user.user_id)
        if oldpwd == user.user_pwd:
            if newpwd == newpwd1:
                if len(newpwd) >= 8 and len(newpwd) <= 16:
                    user1.update(user_pwd = newpwd)
                    return render(req,'user/userloginss.html')
                else:
                    str1 = '密码长度需是8-16位'
                    return render(req,'user/updatePwd.html',{'msg1':str1})
            else:
                str1 = '两次输入的密码不同'
                return render(req, 'user/updatePwd.html' ,{'msg2':str1})
        else:
            str1 = '密码输入不正确'
            return render(req, 'user/updatePwd.html' ,{'msg3':str1})



# 查看收货地址
@require_login1
@csrf_exempt
def addrs(req):
    user_id = req.session['LoginUser'].user_id
    addrs = models.Rec.recmanage.filter(user_id=user_id)
    return render(req, 'user/addrs.html', {'addrs': addrs})


# 添加收货地址
@csrf_exempt
def addAddr(req):
    if req.method == 'GET':
        return render(req, 'user/addAddr.html' )
    else:
        rec_name = req.POST['rec_name']
        rec_phone = req.POST['rec_phone']
        rec_country = req.POST['rec_country']
        rec_pro = req.POST['rec_pro']
        rec_city = req.POST['rec_city']
        rec_area = req.POST['rec_area']
        rec_deta = req.POST['rec_deta']
        user_id = req.session['LoginUser'].user_id
        #创建addr
        if len(rec_phone) ==11:
            print(user_id)
            naddr = models.Rec(rec_name=rec_name,rec_phone=rec_phone,rec_country=rec_country,rec_pro=rec_pro,rec_city=rec_city,rec_area=rec_area,rec_deta=rec_deta,user_id_id=user_id)
            naddr.save()
            return redirect(reverse('user:addrs'))
        else:
            str1 = '联系方式必须的是11位'
            return render(req,'use/addAddr.html',{'msg':str1})


# 检索商品
@require_login1
@csrf_exempt
def allGoods(req):
    Good = []
    Sgood = []
    #检索出应用中所有的商店
    allStores = Stores.storemanage.all()
    # return HttpResponse(allStores)
    for s in allStores:
        # 检索出所有的商店的商品
        allGood_info = Goods_info.goodinfo.filter(store_id_id=s.store_id)
        Sgood.append(allGood_info)
        for g in allGood_info:
            # 检索出对应的商品的详细信息
            good = Goods_mes.goodmesmanage.get(good_id=g.good_id_id)
            if good not in Good:
                Good.append(good)
    return render(req,'user/u_allgoods.html',{'Sgood':Sgood,'Good':Good})




# 检索商品通过商品分类，检索商品名字
@csrf_exempt
def searchGoods(req):
    goods = []
    name = req.POST['q']
    goodkind = Good_kind.goodkingmanager.filter(first=name)
    if len(goodkind) == 0:
        goodkind = Good_kind.goodkingmanager.filter(second=name)
        if len(goodkind) == 0:
            goodkind = Good_kind.goodkingmanager.filter(third=name)
            if len(goodkind) == 0:
                goodkind = Good_kind.goodkingmanager.filter(active1=name)
                if len(goodkind) == 0:
                    goodkind = Good_kind.goodkingmanager.filter(active2=name)
                    if len(goodkind) == 0:
                        str1 = '空空如也'
                        return render(req,'user/searchGoods.html', {'msg':str1})
    # 检索出来类型对应的商品
    for g in goodkind:
        goodinfo = Goods_info.goodinfo.filter(good_id_id=g.good_id_id)
        for i in goodinfo:
            # 检索出对应的商品的店铺的信息等信息,
            s = {'store_id':i.store_id_id,'good_id':i.good_id_id,'sale_num':i.sale_num,'rema_num':i.rema_num}
            goods1 = Goods_mes.goodmesmanage.get(good_id=i.good_id_id)
            # 商品的名字，图片，价格，店铺id，商品id,商品介绍，销量，库存
            s['good_name'] = goods1.good_name
            s['good_img'] = goods1.good_img
            s['good_price'] = goods1.good_price
            s['good_inst'] = goods1.good_inst
            goods.append(s)
        return render(req, 'user/searchGoods.html',{'goods':goods})
		


# 购买
@require_login1
@csrf_exempt
def buyGoods(req,good_id,store_id):
    # 收货地址
    # 购买商品的价钱
    # 购买的商品的
        # 人物id
        user_id = req.session['LoginUser'].user_id
        # 商品的价钱
        good_price = Goods_mes.goodmesmanage.get(good_id=good_id).good_price
        # 人物地址
        adds = models.Rec.recmanage.filter(user_id_id=user_id)
        return render(req,'user/buyGoods.html',{'good_price':good_price, 'adds':adds,'good_id':good_id,'store_id':store_id})



# 提交订单：
@csrf_exempt
def postOrder(req,good_id,store_id):
    user = req.session['LoginUser']
    good_num = req.POST.get('buy_num')
    addr = req.POST['addr']
    good_price = req.POST['good_price']
    # 查找商店的库存,判断购买量是否超出库存
    goods_num = Goods_info.goodinfo.filter(good_id_id=good_id, store_id_id=store_id)
    if int(good_num) > int(goods_num[0].rema_num):
        str1 = '店铺库存不足，请重新选择'
        user_id = req.session['LoginUser'].user_id
        # 商品的价钱
        good_price = Goods_mes.goodmesmanage.get(good_id=good_id).good_price
        # 人物地址
        adds = models.Rec.recmanage.filter(user_id_id=user_id)
        return render(req, 'user/buyGoods.html',
                      {'good_price': good_price, 'adds': adds, 'good_id': good_id, 'store_id': store_id,'msg':str1})

    else:
        # 商店的库存量足够，可以支持购买，
        # 需要写出确认订单的时候的地址，姓名，联系电话，购买商品名称，购买总价
        allprice = int(good_price) * int(good_num)
        print(allprice)
        good = Goods_mes.goodmesmanage.filter(good_id=good_id)
        good_name = good[0].good_name

        return render(req, 'user/submitOrder.html',
                      {'str1': addr, 'total': allprice, 'good_name': good_name, 'store_id': store_id,
                       'good_id': good_id, 'good_num': good_num})



# # 购买
# @require_login1
# @csrf_exempt
# def buyGoods(req,good_id,store_id):
#     # 收货地址
#     # 购买商品的价钱
#     # 购买的商品的
#     if req.method == 'GET':
#         # 人物id
#         user_id = req.session['LoginUser'].user_id
#         # 商品的价钱
#         good_price = Goods_mes.goodmesmanage.get(good_id=good_id).good_price
#         # 人物地址
#         adds = models.Rec.recmanage.filter(user_id_id=user_id)
#         return render(req,'user/buyGoods.html',{'good_price':good_price, 'adds':adds,'good_id':good_id,'store_id':store_id})
#     else:
#         user = req.session['LoginUser']
#         good_num = req.POST.get('buy_num')
#         addr = req.POST['addr']
#         good_price = req.POST['good_price']
#         # 查找商店的库存,判断购买量是否超出库存
#         goods_num = Goods_info.goodinfo.filter(good_id_id = good_id,store_id_id = store_id)
#         if int(good_num) > int(goods_num[0].rema_num):
#             str1 = '店铺库存不足，请重新选择'
#             return redirect(reverse('user:buyGoods',kwargs={'good_id':good_id,'store_id':store_id}))
#         else:
#         #商店的库存量足够，可以支持购买，
#         # 需要写出确认订单的时候的地址，姓名，联系电话，购买商品名称，购买总价
#             allprice = int(good_price) * int(good_num)
#             print(allprice)
#             good = Goods_mes.goodmesmanage.filter(good_id=good_id)
#             good_name = good[0].good_name
# 
#             return render(req, 'user/submitOrder.html' ,{'str1':addr,'total':allprice,'good_name':good_name,'store_id':store_id,'good_id':good_id,'good_num':good_num})


# 查看历史订单
@require_login1
def lookOrder(req):
    order = []
    user = req.session['LoginUser']
    orders = Orders.ordermanager.filter(user_id_id=user.user_id)
    for o in orders:
        addr = o.ord_user_addr
        good_name =Goods_mes.goodmesmanage.filter(good_id = o.good_id_id)[0].good_name
        good_num = o.ord_good_num
        total = o.ord_good_price
        s={'addr':addr,'good_name':good_name,'good_num':good_num,'total':total}
        order.append(s)
    return render(req,'user/lookOrder.html',{'order': order})




# 生成订单
@require_login1
@csrf_exempt
def createOrder(req,good_id,store_id):
    addr = req.POST['addr']
    good_name = req.POST['good_name']
    good_num = req.POST['good_num']
    total = req.POST['total']
    #生成订单，首先在卖家的店铺的销量增加，库存减少，再生成订单
    good_info = Goods_info.goodinfo.filter(good_id_id=good_id,store_id_id=store_id)
    sale_num = good_info[0].sale_num+int(good_num)
    rema_num = good_info[0].rema_num-int(good_num)
    good_info.update(sale_num=sale_num,rema_num=rema_num)

    #生成订单
    user_id = req.session['LoginUser'].user_id
    norder = Orders(ord_good_num=good_num,ord_good_price=total,ord_user_addr=addr,good_id_id=good_id,user_id_id=user_id)
    norder.save()
    # return render(req,'user/orderSus.html')
    # return redirect(reverse('user:lookOrder'))
	
	
	
# 添加到购物车:在满足添加的商品数量小于库存量的时候，将商品添加到购物车，即创建购物车
@require_login1
def addCart(req,good_id,store_id):
    # 商品id，商店id，店铺id，商品数量，单条商品总价
    # 如果购物车里面存在同样的商品id，同样的商店id，同一个userid，则对这条购物车做更改，如果不存在，则创建
    user_id = req.session['LoginUser'].user_id
    cart = Cart.cartmanager.filter(user_id_id=user_id,store_id_id=store_id,good_id_id=good_id)
    good_info = Goods_info.goodinfo.filter(good_id_id=good_id,store_id_id=store_id)
    if len(cart) == 0:
        # 创建
        if good_info[0].rema_num >=1:
            cart_single = Goods_mes.goodmesmanage.filter(good_id=good_id)[0].good_price
            ncart = Cart(good_id_id=good_id,store_id_id =store_id,user_id_id = user_id,cart_good_num=1,cart_single=cart_single)
            ncart.save()
            return redirect(reverse('user:u_allgoods'))
        else:
            # TODO
            str = '库存不足'
            good = Goods_mes.goodmesmanage.filter(good_id=good_id)
            good_name = good[0].good_name
            return render(req, 'user/notEnough.html',{'msg':str,'good_name':good_name})
    else:
        if good_info[0].rema_num >= 1:
            # 做更改,没点击一下添加到购物车，即往购物车里面的添加一个商品，即在原来的基础上加一，也就是将价钱和数量变动一下
            cart_good_num = cart[0].cart_good_num+1
            good_price = Goods_mes.goodmesmanage.filter(good_id=good_id)[0].good_price
            cart_single = good_price*cart_good_num
            # 变动一下价格和数量量
            cart.update(cart_good_num=cart_good_num,cart_single=cart_single)
            return redirect(reverse('user:u_allgoods'))
        else:
            # TODO
            str1 = '库存不足，不能添加购物车'
            good = Goods_mes.goodmesmanage.filter(good_id=good_id)
            good_name = good[0].good_name
            return render(req, 'user/notEnough.html',{'msg':str1,'good_name':good_name})



#查看购物车:列出该用户的购物车里面的所有信息，商品名字，数量，删除，店铺这张表的最下方有一个总价，后面有一个提交订单
@require_login1
def lookCart(req):
    cart = []
    user_id = req.session['LoginUser'].user_id
    carts = Cart.cartmanager.filter(user_id_id=user_id)
    if len(carts) == 0:
        str1 = '空空如也！'
        return render(req,'user/lookCart.html', {'msg':str1})
    else:
        for c in carts:
        #商品的图片，名字，数量，总价，单价
            good = Goods_mes.goodmesmanage.get(good_id = c.good_id_id)
            c_id = c.cart_id
            c_good_id = c.good_id_id
            c_img = good.good_img
            c_name = good.good_name
            c_price = good.good_price
            c_num = c.cart_good_num
            c_total = c.cart_single
            c={'c_id':c_id,'c_good_id':c_good_id,'c_img':c_img,'c_name':c_name,'c_price':c_price,'c_num':c_num,'c_total':c_total}
            cart.append(c)
        return render(req, 'user/lookCart.html', {'cart':cart})


# 删除购物车
@require_login1
def delCart(req,c_id):
    delc = Cart.cartmanager.filter(cart_id=c_id)
    delc.delete()
    return redirect(reverse('user:lookCart'))


# 提交商品，到付款页面
@require_login1
@csrf_exempt
def cartOrder(req):
    if req.method == 'GET':
        # 地址
        addrs = models.Rec.recmanage.filter(user_id_id=req.session['LoginUser'].user_id)
        cart = []
        user_id = req.session['LoginUser'].user_id
        carts = Cart.cartmanager.filter(user_id_id=user_id)
        for c in carts:
        #商品的图片，名字，数量，总价，单价，店铺
            good = Goods_mes.goodmesmanage.get(good_id = c.good_id_id)
            c_id = c.cart_id
            c_store_id = c.store_id_id
            c_good_id = c.good_id_id
            c_img = good.good_img
            c_name = good.good_name
            c_price = good.good_price
            c_num = c.cart_good_num
            c_total = c.cart_single
            c={'c_id':c_id,'c_good_id':c_good_id,'c_store_id':c_store_id,'c_img':c_img,'c_name':c_name,'c_price':c_price,'c_num':c_num,'c_total':c_total}
            cart.append(c)
        req.session['cartOrder'] =cart
        return render(req, 'user/cartOrder.html', {'cart':cart,'addrs':addrs})
    else:
        good = []
        sum = 0
        addrs = req.POST['addr']
        goods = req.POST.getlist('cd')
        # 删除勾选的这条购物车
        print(goods)
        cart = req.session['cartOrder']
        for g in goods:
            s=g.split(' ')
            sum+=int(s[2])
            good.append(s)
        for g in good:
            for c in cart:
                if c['c_name'] == g[0] and c['c_store_id'] == int(g[3]):
                    print(123)
                    c_id = c['c_id']
                    print(c_id)
                    delc = Cart.cartmanager.filter(cart_id=c_id)
                    delc.delete()
        return render(req,'user/submitCart.html',{'addrs':addrs,'good':good,'sum':sum})



# 购物里面的生成订单
# 购物里面的生成订单,在store里面的good_info里面销售数量增加，库存数量减少
@require_login1
@csrf_exempt
def prodectOrder(req):
    user_id = req.session['LoginUser'].user_id
    addr = req.POST['addr']
    good = req.session['cartOrder']
    for g in good:
        print(g['c_good_id'], type(g['c_good_id']))
        good_id = g['c_good_id']
        #生成订单
        norder = Orders(good_id_id=good_id,user_id_id=user_id,ord_user_addr=addr,ord_good_price=g['c_total'],ord_good_num=g['c_num'])
        norder.save()
        #good_info里面的商品库存量减少，商店销售数量增加
        store_id = g['c_store_id']
        num = g['c_num']
        good_info = Goods_info.goodinfo.filter(store_id_id=store_id,good_id_id=good_id)
        rema = good_info[0].rema_num - num
        sale = good_info[0].sale_num + num
        good_info.update(sale_num=sale,rema_num = rema)
    del req.session['cartOrder']
    return redirect(reverse('user:lookOrder'))



# @require_login1
# @csrf_exempt
# def prodectOrder(req):
#     user_id = req.session['LoginUser'].user_id
#     addr = req.POST['addr']
#     good = req.session['cartOrder']
#     for g in good:
#         goods = Goods_mes.goodmesmanage.get(good_name=g[0])
#         good_id = goods.good_id
#         #生成订单
#         norder = Orders(good_id_id=good_id,user_id_id=user_id,ord_user_addr=addr,ord_good_price=g[2],ord_good_num=g[1])
#         norder.save()
#     del req.session['cartOrder']
#     return redirect(reverse('user:lookOrder'))
	


# 进入店铺
@require_login1
def enterShop(req,store_id):
     goods = Goods_info.goodinfo.filter(store_id=store_id)
     # 查找店铺，检索店铺的详细信息
     store = Stores.storemanage.filter(store_id=store_id)[0]
     gs = []
     print(len(goods))
     for i in goods :
         # 找出相应的货物
         s = Goods_mes.goodmesmanage.get(good_id = i.good_id_id)
         # print(i,i.store_id_id)
         sd = {'sotre_id':i.store_id_id,'good_id':i.good_id_id,'sale_num':i.sale_num,'rema_num':i.rema_num,'good_name':s.good_name,'good_price':s.good_price,'good_inst':s.good_inst,'good_img':s.good_img}
         gs.append(sd)
     return render(req, 'user/storeall.html' ,{'gs':gs,'store':store})


# 商品详情
def goodDetal(req ,good_id, store_id):
    # 检查出来商品在店铺里面的详情
    good_info = Goods_info.goodinfo.get(good_id_id=good_id,store_id_id=store_id)
    # 检查商品的详情
    good = Goods_mes.goodmesmanage.get(good_id = good_id)
    return render(req, 'user/goodDetal.html' ,{'good':good, 'good_info':good_info})




# 退出登录
@require_login1
def exitUser(req):
    user_name = req.session['LoginUser'].user_name
    del req.session['LoginUser']
    return render(req, 'user/exitUser.html' ,{'msg': user_name})




