"""mypro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
# from api.views import apitest001,apitest002,apitest003,apitest004,apitest005,apitest006
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # 从根路径开始的路径
#     path('apitest001/', apitest001),
#     path('apitest002', apitest002),
#     path('apitest03', apitest003),
#     path('apitest004', apitest004),
#     path('apitest005/', apitest005),
#     path('apitest006', apitest006),
# ]


from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.decorators import api_view

from api.views import gettags, TestApi, Login,GetID

swagger_info = openapi.Info(
    title="Snippets API",
    default_version='v1',
    description="""This is a demo project for the [drf-yasg](https://github.com/axnsan12/drf-yasg) Django Rest Framework library.

The `swagger-ui` view can be found [here](/cached/swagger).
The `ReDoc` view can be found [here](/cached/redoc).
The swagger YAML document can be found [here](/cached/swagger.yaml).

You can log in using the pre-existing `admin` user with password `passwordadmin`.""",  # noqa
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="contact@snippets.local"),
    license=openapi.License(name="BSD License"),
)

SchemaView = get_schema_view(
    validators=['ssv', 'flex'],
    public=True,
)

@api_view(['GET'])
def plain_view(request):
    pass

# urlpatterns required for settings values
required_urlpatterns = [
    path('admin/', admin.site.urls),
    # 前面一样的路径，叫基础路径
    # 后面不一样的地方，会显示在接口文档的path里面
    path('mypro/api/doc/gettags', gettags),
    path('mypro/api/doc/getid', GetID.as_view()),
    path('mypro/api/doc/testapi', TestApi.as_view()),
    path('mypro/api/user/login', Login.as_view()),
]

urlpatterns = \
    [
        path('mypro/swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('mypro/redoc/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        # path('mypro/plain/', plain_view),
    ] + required_urlpatterns
