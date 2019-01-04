#  绣春刀——无常簿
#
# 查看所有可疑员——http://localhost:8000/findall
# 新增可疑人员——http://localhost:8000/addgood
# 删除可疑人员——http://localhost:8000/deletebad
#  使用wsgi开发处理接口，纯GET方式操作

# 查找所有可疑人员页面


def findall(env,response):
    response('200 ok',[('Content-type','text/html_lib')])
    return ['<h1>这是查找所有的页面</h1>'.encode('gbk')]


# 新增页面
def addgood(env,response):
    response('200 ok',[('Content-type','text/html_lib')])
    return ['<h1>这是新增可疑人物的页面</h1>'.encode('gbk')]


# 删除页面
def deletegood(env,response):
    response('200 ok',[('Content-type','text/html_lib')])
    return ['<h1>这是删除可疑人物的页面</h1>'.encode('gbk')]


from wsgiref.simple_server import make_server


def index(evn,response):
    if evn['PATH_INFO'][1:] == "findall":
        return findall(evn,response)
    elif evn['PATH_INFO'][1:] == "addgood":
        return addgood(evn,response)
    else:
        return deletegood(evn,response)


a=make_server('192.168.12.14',8000,index)
print("贪玩蓝月，启动")
a.serve_forever()
