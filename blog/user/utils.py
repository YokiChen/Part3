import random,string
from PIL import Image,ImageDraw,ImageFont,ImageFilter
def getRandomChar(count=4):
    # 随机生成字符串
    ran = string.ascii_letters+string.digits
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char

# 返回一个随机的 RGB 颜色
def getRandomColor():
    return(random.randint(50,150),random.randint(50,150),random.randint(50,150))

def create_code():
    # 创建图片，模式，大小，背景色
    img = Image.new('RGB', (120,30), (255,255,255))
    #创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype('arial.ttf', 25)

    code = getRandomChar()
     # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30*t+5,0),code[t],getRandomColor(),font)
     # 生成干扰点
    for _ in range(random.randint(0,50)):
    # 位置，颜色
        draw.point((random.randint(0, 120),
            random.randint(0, 30)),fill=getRandomColor())
    # 使用模糊滤镜使图片模糊
    img = img.filter(ImageFilter.BLUR)
    # 保存
    # img.save(''.join(code)+'.jpg','jpeg')
    return img,code


