import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
from api.cases_serializers import UserErrCode,UserInfoSerializer
from api.models import UserInfo
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.apps import logger


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
    query_list = list(UserInfo.objects.filter().values())
    print(query_list)
    return JsonResponse({'code': 0, 'msg': '查询表里面所有的数据'})


def apitest006(request):
    """
    通过GET请求传参，把参数通过数据库查询结果
    通过http://127.0.0.1:8000/apitest006?username=will&pwd=123456测试
    """
    # 接受GET传参
    params = dict(request.GET)  # params={'username': ['jinshan'], 'pwd': ['123']}
    args = {}
    args['username'] = params.get('username')[0]
    args['pwd'] = params.get('pwd')[0]

    # 将变量通过数据库查询
    query_list = list(UserInfo.objects.filter(**args).values())
    print(query_list)
    if query_list:
        # 把密码以***的格式返回
        query_list[0]['pwd'] = '***'
        return JsonResponse({'code': 0, 'msg': '登录成功', 'data': query_list})
    else:
        return JsonResponse({'code': 1, 'msg': '登录fail'})


def gettags(request):
    """作用：用于显示api接口分类下拉列表"""
    return JsonResponse({"code": 200, "msg": "标签加载成功", "data": [{"name": "用户接口"}, {"name": "用例管理"}]})


class GetID(APIView):
    @swagger_auto_schema(
        operation_description='在自动化平台修改一个用例的信息',
        operation_summary='修改用例',
        manual_parameters=[
            # 一个参数的时候不显示
            openapi.Parameter('id', openapi.IN_QUERY, description="需要导出的项目id", type=openapi.TYPE_INTEGER),
            openapi.Parameter('id1', openapi.IN_QUERY, description="需要导出的项目id", type=openapi.TYPE_INTEGER),
        ],

        # responses={210: openapi.Response('response description', UpdateCaseErrCode)},
        tags=['用例管理', 'application/json', 'application/json;'],

    )
    def get(self, request):
        """获取接口分组信息"""
        return JsonResponse({"code": 200, "msg": "标签加载成功", "data": [{"name": "用户接口"}, {"name": "用例管理"}]})


class TestApi(APIView):
    @swagger_auto_schema(
        operation_description='在自动化平台修改一个用例的信息',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='用例id'),
                'casename': openapi.Schema(type=openapi.TYPE_STRING, description='用例名'),
                'stepname': openapi.Schema(type=openapi.TYPE_STRING, description='步骤名'),
                'keywords': openapi.Schema(type=openapi.TYPE_STRING, description='关键字'),
                'params1': openapi.Schema(type=openapi.TYPE_STRING, description='参数1'),
                'params2': openapi.Schema(type=openapi.TYPE_STRING, description='参数2'),
            },
        ),
        responses={210: openapi.Response('response description', UserErrCode)},
        tags=['用例管理', 'application/json', 'application/json;'],
        operation_summary='修改用例',
    )
    def post(self, request):
        """
        登录平台，登录后sessionid会具备登录态
        """
        return JsonResponse({"code": 1001, "msg": '用例id必须是整数'})


class Login(APIView):
    @swagger_auto_schema(
        operation_description='在登录页进行用户名密码登入',
        operation_summary='登录平台',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username','pwd'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='用户名'),
                'pwd': openapi.Schema(type=openapi.TYPE_STRING, description='密码'),
            },
        ),
        # 针对接口http：200 210
        responses={200: openapi.Response('response description', UserInfoSerializer),
                   210: openapi.Response('errorcode description', UserErrCode)},
        tags=['用户接口', 'application/json', 'application/json;'],
        # tags=['用户接口', 'application/x-www-form-urlencoded', 'application/json;'],
    )
    def post(self, request):
        """
        登录平台，登录后sessionid会具备登录态
        """
        # json.loads()是用来把字符串变为dict
        kwargs = json.loads(request.body)
        # print(type(kwargs))
        # print(kwargs)
        logger.info(kwargs)
        # kwargs = {'username': 'will', 'pwd': '123456'}
        query_data = list(UserInfo.objects.filter(**kwargs).values())
        if query_data:
            return JsonResponse({"code": 1000, "msg": '登录成功', 'data': query_data})
        else:
            return JsonResponse({"code": 1001, "msg": '用户名密码错误'})
