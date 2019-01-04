# 写方法，跳转的页面，方法名字为跳转的网页的后缀
def index(evn,response):
    # print(evn,response)
    response('200 ok', [('Content-type', 'text/html_lib')])
    if evn['PATH_INFO'][1:] == "findall":
        return ['<h1>这是查找所有的页面</h1>'.encode('gbk')]
    elif evn['PATH_INFO'][1:] == "addgood":
        return ['<h1>这是新增可疑人物的页面</h1>'.encode('gbk')]
    else:
        return ['<h1>这是删除可疑人物的页面</h1>'.encode('gbk')]
    # 设置返回文本的方式，200为ok，链接成功[]内为文本的格式（只有文本格式正确，才能返回正确的内容）
    # response('200 ok',[("Content-type", "text/html_lib")])
    # return [b'<h1 style="color: red">hello,python</h1>']
# 导入包，从wsgi的简单服务里导入制作服务模块
from wsgiref.simple_server import make_server

a=make_server('192.168.12.14',20000,index)
print("启动了")
a.serve_forever()