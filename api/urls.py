"""ticks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import inspect
from django.apps import apps
from django.urls import path, re_path
from django.conf.urls import include
from django.conf import settings
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_bulk.routes import BulkRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from api.views.accountViewSet.User import UserViewSet, MiniUserViewSet
from api.views import accountViewSet, utilsViewSet, auditlogViewSet, WMSViewSet
from api.views.user_action import RegisterView, ResetPasswordView, ValidView
from api.views.WMSViewSet import WmsInventoryCheckDetailViewSet, WmsInventoryMovementDetailViewSet, \
    WmsReceiptOrderDetailViewSet, WmsShipmentOrderDetailViewSet
from api.views.accountViewSet.UserPermission import GetUserPermissionViewSet
from api.views.accountViewSet.UIRouter import GetRouterViewSet
from api.serializers.token_auth import CustomTokenObtainPairSerializer

# 走批量接口支持不带 id 更新
bulk_router = BulkRouter()
bulk_router.register(r'wmsinventorycheckdetail',
                     WmsInventoryCheckDetailViewSet)
bulk_router.register(r'wmsinventorymovementdetail',
                     WmsInventoryMovementDetailViewSet)
bulk_router.register(r'wmsreceiptorderdetail', WmsReceiptOrderDetailViewSet)
bulk_router.register(r'wmsshipmentorderdetail', WmsShipmentOrderDetailViewSet)

# 默认权限
# router = routers.DefaultRouter()
# 不显示 router 列表页面
router = routers.SimpleRouter()
router.register("user", UserViewSet)
# 一些公共权限使用，只提供基础信息
router.register("mini_user", MiniUserViewSet)

exclude_viewSet_list = [UserViewSet, WmsInventoryCheckDetailViewSet, WmsInventoryMovementDetailViewSet,
                        WmsReceiptOrderDetailViewSet, WmsShipmentOrderDetailViewSet]

# 用来判定注册时候 ViewSet 是不是原生默认的 ViewSet，防止自定义 ViewSet 覆盖原生 model 同名 ViewSet， 此代码修复了如下 bug
# old, 已经 fix: 注意⚠️，这里有BUG， 非默认 ViewSet 不要写在 ViewSet/__init__ 里面
default_model_name = []
for index, model in enumerate(apps.get_models()):
    if model._meta.model_name not in default_model_name:
        default_model_name.append(model._meta.model_name)

for view in [accountViewSet, utilsViewSet, WMSViewSet]:
    for name, obj in inspect.getmembers(view):
        if inspect.isclass(obj) and obj not in exclude_viewSet_list:
            # 只注册小写同名 ViewSet, 自行编写的 ViewSet 请 register
            model_name = str(obj).split(
                ".")[-1].replace("ViewSet\'>", "").lower()
            if model_name in default_model_name:
                url_name = str(obj).split(".")[-2].lower()
                router.register(url_name, obj, basename=url_name)

# router.register("action_log", auditlogViewSet.LogEntryViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="openWMS API文档",
        default_version='v1',
        description="openWMS API文档",
        terms_of_service="http://www.precisiongenes.com.cn/",
        contact=openapi.Contact(email="iqinfei@163.com"),
        license=openapi.License(name="GPL v3"),
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
)

# router.register("action_log", auditlogViewSet.LogEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(bulk_router.urls)),
    # 允许登录 drf 控制台， INSTALL_APPS 里面的 drf 为了能够出现控制台界面
    # path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='register'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('get_valid/', ValidView.as_view(), name='valid'),
    path('get_permission/', GetUserPermissionViewSet.as_view(),
         name='get_permission'),
    path('get_router/', GetRouterViewSet.as_view(), name='get_router'),
]

if settings.VAPTCHA_IN_API_AUTH:
    urlpatterns += [
        path('token-auth/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer),
             name='token-auth'),
    ]
else:
    urlpatterns += [
        path('token-auth/', TokenObtainPairView.as_view(),
             name='token-auth'),
    ]


# 正式上线之后关闭文档
# if settings.DEBUG:
urlpatterns += [
    re_path(r'swagger(?P<format>\.json|\.yaml)',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path(r'docs/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
