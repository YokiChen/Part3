from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from User.views import createimg
from User import util1
from . import models
import Goods.models
# Create your views here.

# 首页
def storeIndex(req):
    return render(req,'store/index.html')


# 注册成为店主
@csrf_exempt
def Shopowner(req):
    if req.method == 'GET':
        return render(req, 'store/Shopowner.html')
    else:
        seller_name = req.POST['seller_name']
        seller_phone = req.POST['seller_phone']

        seller_pwd = req.POST['seller_pwd']
        seller_pwd_again = req.POST['seller_pwd_again']
        code = req.POST['code']
        seller = models.Seller.sellermanager.filter(seller_phone=seller_phone)
        if req.session['check_code'] == code:
            if len(seller) == 0 :
                if len(seller_pwd)>8 and len(seller_pwd)<16:
                    if seller_pwd == seller_pwd_again:
                        if len(seller_phone)==11:
                            try:
                                seller_header = req.FILES['seller_header']
                                nseller = models.Seller(seller_account = 'gc',seller_name = seller_name,seller_phone=seller_phone,seller_header=seller_header,seller_pwd=seller_pwd )
                                nseller.save()
                                return redirect(reverse('store:SellerLogin'))
                            except:
                                nseller = models.Seller(seller_account='gc', seller_name=seller_name,
                                                        seller_phone=seller_phone, seller_header='null',
                                                        seller_pwd=seller_pwd)
                                nseller.save()
                                return redirect(reverse('store:SellerLogin'))
                        else:
                            str1 = '手机联系方式应有11位'
                            return render(req, 'store/Shopowner.html', {'msg1': str1})
                    else:
                        str1 = '两次输入的密码不同，请重新输入'
                        return render(req, 'store/Shopowner.html', {'msg2': str1})
                else:
                    str1 = '登录密码长度应该在8-16位'
                    return render(req, 'store/Shopowner.html', {'msg3': str1})
            else:
                str1 = '该手机号已经注册过了'
                return render(req, 'store/Shopowner.html', {'msg4': str1})
        else:
            str1 = '验证码错误，请重新输入'
            return render(req, 'store/Shopowner.html' , {'msg5':str1})



# 店家登录
@csrf_exempt
def SellerLogin(req):
    if req.method == 'GET':
        return render(req, 'store/sellerLogin.html')
    else:
        seller_phone = req.POST['seller_phone']
        seller_pwd = req.POST['seller_pwd']
        code = req.POST['code']
        seller = models.Seller.sellermanager.filter(seller_phone=seller_phone)
        if req.session['check_code'] == code:
            if len(seller)!=0:
                if seller_pwd == seller[0].seller_pwd:
                    req.session['sellerLogin'] = seller[0]
                    return redirect(reverse('store:allStore'))
                else:
                    str1 = '密码错误'
                    return render(req, 'store/sellerLogin.html', {'msg1':str1})
            else:
                str1 = '店家不存在'
                return render(req, 'store/sellerLogin.html', {'msg2':str1})
        else:
            str1 = '验证码错误，请重新输入'
            return render(req, 'store/sellerLogin.html', {'msg3':str1})

# 装饰器 判断登陆状态/未实现，
def require_login1(fn):
    def inner_fn(req, *args, **keyargs):
        if req.session.has_key('sellerLogin'):
            result = fn(req,*args, **keyargs)
            return result
        else:
            return redirect("/store/SellerLogin/")
    return inner_fn


# 店铺注册
@csrf_exempt
def StoreReg(req):
    if req.method == 'GET':
        return render(req, 'store/StoreReg.html')
    else:
        store_name = req.POST['store_name']
        
        store_deta = req.POST['store_deta']
        seller_id = req.session['sellerLogin'].seller_id
        code = req.POST['code']
        store1 = models.Stores.storemanage.filter(store_name=store_name)
        if len(store1) == 0:
            if req.session['check_code'] == code:
                try:
                    store_pic = req.FILES['store_pic']
                    nstore = models.Stores(store_name=store_name,store_pic=store_pic,store_deta=store_deta,seller_id_id=seller_id)
                    nstore.save()
                    return redirect(reverse('store:allStore'))
                except:
                    nstore = models.Stores(store_name=store_name, store_pic='null', store_deta=store_deta,
                                           seller_id_id=seller_id)
                    nstore.save()
                    return redirect(reverse('store:allStore'))
            else:
                str1 = '验证码错误，请重新输入'
                return render(req, 'store/StoreReg.html', {'msg':str1})
        else:
            str1 = '该店名已存在，请重新输入'
            return render(req,'store/StoreReg.html', {'msg':str1})


# 查看所有店铺
@require_login1
def allStore(req):
    seller_id = req.session['sellerLogin'].seller_id
    stores = models.Stores.storemanage.filter(seller_id=seller_id)
    print(stores)
    return render(req, 'store/allstore.html', {'stores':stores})


# 进入店铺
@require_login1
def onestore(req,store_id):
    return render(req, 'store/onestore.html', {'store_id':store_id})


@require_login1
@csrf_exempt
def uploadGoods(req,store_id):
    if req.method == 'GET':
        return render(req, 'store/uploadGoods.html', {'store_id':store_id})
    else:
        print(store_id)
        # good_id =
        # 商品相关信息
        good_name = req.POST['good_name']
        good_price = req.POST['good_price']
        good_inst = req.POST['good_inst']

        # 商品类型相关信息
        first = req.POST['first']
        second = req.POST['second']
        third = req.POST['third']
        active1 = req.POST['active1']
        active2 = req.POST['active2']
        # 店铺里面的商品的相关信息
        sale_num = req.POST['sale_num']
        rema_num = req.POST['rema_num']
        # store_id = req.POST['store_id']
        good = Goods.models.Goods_mes.goodmesmanage.filter(good_name=good_name)
        # 商品名字不能重复
        if len(good) == 0:
            #没有这个商品,创建商品
            try:
                good_img = req.FILES['good_img1']
                ngood = Goods.models.Goods_mes(good_name=good_name,good_price=good_price,good_inst=good_inst,good_img=good_img)
                ngood.save()
            except:
                ngood = Goods.models.Goods_mes(good_name=good_name, good_price=good_price, good_inst=good_inst,
                                               good_img='null')
                ngood.save()
            #创建相应的类型
            good_id=ngood.good_id
            nkind = Goods.models.Good_kind(first=first,second=second,third=third,active1=active1,active2=active2,good_id_id=good_id)
            nkind.save()
            #创建店铺里面的商品信息
            # store = models.Stores.storemanage.filter(store_id=store_id)
            ngood_info = models.Goods_info(sale_num=sale_num, rema_num =rema_num, store_id_id=store_id,good_id_id = good_id)
            ngood_info.save()
            return render(req, 'store/onestore.html' ,{'store_id':store_id})

        else:
            #已经有这个商品了
            good_id = good[0].good_id
            ngood_info = models.Goods_info(sale_num=sale_num, rema_num=rema_num, store_id_id=store_id,good_id_id=good_id)
            ngood_info.save()
            return render(req, 'store/onestore.html', {'store_id':store_id})



# 修改商品。但是商家只能修改数量和库存数量
@require_login1
@csrf_exempt
def  updateGoods(req,store_id,good_id):
    if req.method == 'GET':
        old_goodinfo = Goods.models.Goods_mes.goodmesmanage.get(good_id=good_id)
        old_kind = models.Goods_info.goodinfo.filter(store_id_id=store_id,good_id_id=good_id)[0]
        return render(req, 'store/updateGoods.html', {'store_id':store_id, 'good_id':good_id,'old_goodinfo':old_goodinfo,'old_kind':old_kind})
    else:
        # sale_num = req.POST['sale_num']
        rema_num = req.POST['rema_num']
        good_price = req.POST['good_price']
        #检索出店铺商品信息。然后更新
        good = models.Goods_info.goodinfo.filter(store_id_id=store_id,good_id_id=good_id)
        # ugood = good.update(sale_num=sale_num,rema_num=rema_num)
        ugood = good.update(rema_num=rema_num)
        # print(req.session['old_sale_num'])

        # 找到商品的信息，并且更新
        good1 = models.Goods_mes.goodmesmanage.filter(good_id=good_id)
        ngood = good1.update(good_price = good_price)

        return redirect(reverse('store:s_allGoods',kwargs={'store_id':store_id}))



# 查看店铺的所有商品
@require_login1
@csrf_exempt
def s_allGoods(req,store_id):
    goods = models.Goods_info.goodinfo.filter(store_id=store_id)
    gs = []
    print(len(goods))
    for i in goods :
        # 找出相应的货物
        s = Goods.models.Goods_mes.goodmesmanage.get(good_id = i.good_id_id)
        print(i,i.store_id_id)
        sd = {'sotre_id':i.store_id_id,'good_id':i.good_id_id,'sale_num':i.sale_num,'rema_num':i.rema_num,'good_name':s.good_name,'good_price':s.good_price,'good_inst':s.good_inst, 'good_img':s.good_img}
        gs.append(sd)
    return render(req, 'store/s_allGoods.html' ,{'gs':gs,'store_id':store_id})


# 下架商品,直接让商品的销售数量和库存为0
@require_login1
def undercarriage(req,store_id,good_id):
    sale_num = 0
    rema_num = 0
    good = models.Goods_info.goodinfo.filter(store_id_id=store_id, good_id_id=good_id)
    ugood = good.update(sale_num=sale_num, rema_num=rema_num)
    return redirect(reverse('store:s_allGoods', kwargs={'store_id': store_id}))
		
		
		
# 店家退出登录
@require_login1
def exitSeller(req):
    seller_name = req.session['sellerLogin'].seller_name
    del req.session['sellerLogin']
    return render(req, 'store/exitSeller.html', {'msg': seller_name})