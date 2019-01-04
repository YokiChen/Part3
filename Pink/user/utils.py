"""
工具模块
"""
from django.shortcuts import redirect

from hashlib import md5

from PIL import Image, ImageDraw, ImageFont, ImageFilter

import string, random

import hmac, re

from . import models

salt_key = "huang_yuan"


def json_object(object):
    return {
        "user_id": object.user_id,
        "user_name": object.user_name,
        "user_password": object.user_password,
        "user_nickname": object.user_nickname,
        "user_age": object.user_age,
        "user_gender": object.user_gender,
        "user_email": object.user_email,
        "avatar": object.avatar.__str__()}


def require_login(fn):
    def inner_fn(request, *args, **keyargs):
        if request.session.has_key("loginUser"):
            result = fn(request)
            return result
        else:
            return redirect("/index/login_out/")
    return inner_fn


def md5_hashlib_user(key, salt=salt_key):
    md_user = md5(key.encode())
    md_user.update(salt.encode())
    return md_user.hexdigest()


def md5_hmac_user(key, salt=salt_key):
    md_user = hmac.new(salt.encode(), key.encode(), "MD5")
    return md_user.hexdigest()


def get_random_char(count=4):
    """生成随机字符串,建议有什么比较好用的直接用不能学习老师，明明有一个可好用的字段不用"""
    ran_ser = string.ascii_letters+string.digits
    char = ""
    for i in range(count):
        char += random.choice(ran_ser)
    return char


def get_random_color():
    return (random.randint(50,150), random.randint(50,150), random.randint(50,150))


def create_code():
    """创建一个图片"""
    # 创建图片模式大小背景色
    img = Image.new('RGB', (120, 30), (10, 10, 10))
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype('arial.ttf', 25)

    code = get_random_char()
    for t in range(4):
        draw.text((30*t+5, 0), code[t], get_random_color(), font)
    # 生成干扰点
    for i in range(random.randint(0,50)):
        draw.point((random.randint(0, 120), random.randint(0, 30)), fill=get_random_color())
    # 使用模糊滤镜使图片模糊
    img = img.filter(ImageFilter.SMOOTH_MORE)
    # 保存
    # img.save("img_random", "png")
    return img, code


def remove_html_by_re(content):
    """使用正则去除字符串的html标签，传入content"""
    pattern = r"</?(.*?)>"
    content = re.sub(pattern, "", content)

    return content


def register_tool(request):
    kwd = False
    if not request.POST["user_id"].isalnum():
        return kwd, "账户id不合法"
    if len(request.POST["user_id"]) < 6:
        return kwd, "账户id过短"
    if len(request.POST["user_id"]) > 18:
        return kwd, "账户id过长"
    if len(request.POST["user_pwd"]) < 6:
        return kwd, "用户密码过短"
    if len(request.POST["user_pwd"]) > 18:
        return kwd, "用户密码过长"
    if request.POST["user_pwd"] != request.POST["user_con_pwd"]:
        return kwd, "两次输入密码不一致"
    if len(models.User.objects.filter(pk=request.POST["user_id"])) == 1:
        return kwd, "该账户已经存在，请重新设置id"
    kwd = True
    return kwd, "验证通过"


def request_style(request):
    if request.method == "GET":
        return 1
    else:
        return 2









