from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
from api.models import UserInfo1


def apitest001(request):
    """
    这是一个返回template模板的view函数
    """
    return render(request, 'index.html')  # 返回index.html文件到前端


def apitest002(request):
    """这是一个接口"""
    return HttpResponse('你好')


def apitest003(request):
    """返回json格式"""
    return JsonResponse({'code': 1, 'msg': '恭喜您'})


def apitest004(request):
    """
    GET类型传参
    在浏览器里访问：http://127.0.0.1:8000/apitest004?username=jin&pwd=123
    """
    # 将<QueryDict: {'username': ['jinshan'], 'pwd': ['123']}>转为dict类型
    params = dict(request.GET)
    # params={'username': ['jinshan'], 'pwd': ['123']}
    print(params)
    v = params.get('username')[0]
    print(v)
    if v == 'jin':
        return JsonResponse({'code': 1, 'msg': '恭喜您'})
    else:
        return JsonResponse({'code': -1, 'msg': '谢谢惠顾'})


def apitest005(request):
    """连接数据库，查询语句"""
    # 将查询结果转为list列表
    query_list = list(UserInfo1.objects.filter().values())
    print(query_list)
    return JsonResponse({'code': 0, 'msg': '查询表里面所有的数据'})


def apitest006(request):
    """
    通过GET请求传参，把参数通过数据库查询结果
    通过http://127.0.0.1:8000/apitest006?username=will&pwd=123456测试
    """
    # 接受GET传参
    params = dict(request.GET) # params={'username': ['jinshan'], 'pwd': ['123']}
    args={}
    args['username'] = params.get('username')[0]
    args['pwd'] = params.get('pwd')[0]

    # 将变量通过数据库查询
    query_list = list(UserInfo1.objects.filter(**args).values())
    print(query_list)
    if query_list:
        # 把密码以***的格式返回
        query_list[0]['pwd'] = '***'
        return JsonResponse({'code': 0, 'msg': '登录成功', 'data': query_list})
    else:
        return JsonResponse({'code': 1, 'msg': '登录fail'})
