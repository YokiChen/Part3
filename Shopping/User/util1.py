import random, string
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def getRandomChar(count=4):
    # 生成随机字符串
    # string 模块包含各种字符串，以下为小写字母加数字
    ran = string.ascii_lowercase + string.digits
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char


# 返回一个随机的 RGB 颜色
def getRandomColor():
    return (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))


def create_code():
    # 创建图片，模式，大小，背景色
    img = Image.new('RGB', (150, 40), (255,255,255))
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype('font1/arial.ttf', 30)

    code = getRandomChar()
    # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30 * t + 10, 4), code[t], getRandomColor(), font)
    # 生成干扰点
    for _ in range(random.randint(25, 50)):
        # 位置，颜色
        draw.point((random.randint(0, 120), random.randint(0, 80)), fill=getRandomColor())
    # 使用模糊滤镜使图片模糊
    img = img.filter(ImageFilter.BLUR)
    # 保存
    # img.save(''.join(code)+'.jpg','jpeg')
    return img, code

# if __name__=='main':
# print(create_code())
