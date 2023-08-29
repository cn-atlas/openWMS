"""
注册、邮件验证、手机验证、忘记密码、重置密码
# https://www.cnblogs.com/qx1996liu/p/13888931.html
# https://q1mi.github.io/Django-REST-framework-documentation/api-guide/fields_zh/
"""
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.db.models import Q
from rest_framework.response import Response
from account.models import User
from api.serializers.user_action import RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ValidView(APIView):
    '''
    验证接口 手机号码/邮件，忘记密码、重置密码、用户激活都在这里
    '''
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)
    result = dict()
    result["msg"] = "未知错误!"
    throttle_scope = 'valid'

    def get(self, request):
        """
        传输用户名、邮箱、手机号码等信息先行验证，然后生成一个随机 uuid ，用于用户重置密码的 url 验证

        request 参数 username 和 email(这里不是真正意义的邮箱，请在 placeholder 写 "邮箱/手机号")
        eg: /api/v1/valid/?username=qinfei&email=iqinfei@163.com
        """
        username = request.GET.get("username")
        email = request.GET.get("email")
        # 验证码类型，邮件、微信、钉钉、短信 email/wechat/dingtalk/sms
        msg_type = request.GET.get("type")
        user_query_set = User.objects.filter(Q(mobile=email) | Q(email=email), username=username)
        user = user_query_set.first()
        if user:
            # TODO: 全部放在异步任务里面进行动作
            pass
            # uuid = uuid4()
            # user_query_set.update(uuid=uuid, uuid_time=get_date_time_now_local() + timedelta(hours=2))
            # msg_template = MsgTemplate.objects.filter(subject__icontains="重置密码").first()
            # if msg_template:
            # url = "/".join(request.build_absolute_uri(None).split("/")[:3]) + msg_template.redirect_url + \
            #       "?valid_code={}&username={}&type=2".format(uuid, username)
            # send_email.delay(user.id, msg_template.id, url=url)
            #     self.result["status_code"] = '0'
            #     self.result["msg"] = "重置信息发送完成，请检查您的邮箱！"
            #     return Response(self.result, status=202)
            # else:
            #     self.result["status_code"] = '3'
            #     self.result["msg"] = "系统内部错误，请联系管理员添加通知模板！"
            #     return Response(self.result, status=500)
        else:
            self.result["status_code"] = '1'
            self.result["msg"] = "账户信息填写错误！"
            return Response(self.result, status=404)


class ResetPasswordView(APIView):
    '''
    验证接口 手机号码/邮件，忘记密码、重置密码、用户激活都在这里
    '''
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)
    result = dict()
    result["msg"] = "未知错误!"
    throttle_scope = 'valid'

    def check_password(self, request, user):
        """
        验证密码
        """
        password = request.data.get("password")
        password2 = request.data.get("password2")
        if password != password2:
            self.result["status_code"] = '-2'
            self.result["msg"] = "两次密码不一致！"
            return Response(self.result, status=417)
        # User.objects.filter(id=user.id).update(uuid=None, uuid_time=None)
        user.set_password(password)
        user.save()
        self.result["status_code"] = '0'
        self.result["msg"] = "重置密码成功，请登录！"
        return Response(self.result, status=200)

    def post(self, request):
        """
        重新设置密码接口

        reset_type == 1 的时候 是 重置密码 request get 参数 type=1, post 内容 username old_password password password2
        reset_type == 2 的时候是 valid（邮件、手机验证）,邮件里面 url 里面含有username uuid 读出来之后放到 post里面, request get 参数 type=2, post 内容 username uuid password password2

        返回格式
        {
            "status_code": "{status_code}",
            "msg": "{msg}"
        }

        HTTP 状态码 20x 即是返回成功
        """
        x_type = request.GET.get("reset_type", "1")
        if x_type == "2":
            valid_code = request.data.get("valid_code")
            username = request.data.get("username")
            user = User.objects.filter(username=username, uuid=valid_code).first()
            # if user.uuid_time < get_date_time_now_local():
            #     self.result["status_code"] = '3'
            #     self.result["msg"] = "重置链接已失效，请重新获取！"
            #     return Response(self.result, status=403)
            # if not user:
            #     self.result["status_code"] = '1'
            #     self.result["msg"] = "参数错误！"
            #     return Response(self.result, status=404)
            # return self.check_password(request, user)
        elif x_type == "3":
            # 短信验证重置密码逻辑
            username = request.data.get("username")
            # mobile = request.data.get("mobile")
            valid_code = request.data.get("valid_code")
            user = User.objects.filter(username=username).first()
            if not user:
                self.result["status_code"] = '1'
                self.result["msg"] = "账户信息错误！"
                return Response(self.result, status=404)

            # sms_log_obj = SmsLog.objects.filter(mobile=mobile, valid_code=valid_code, purpose='reset_pwd').first()
            # TODO 重置密码的验证码后面需要加上验证码过期时间
            # if not sms_log_obj:
            #     self.result["status_code"] = '1'
            #     self.result["msg"] = "验证失败！"
            #     return Response(self.result, status=404)

            return self.check_password(request, user)

        else:
            username = request.data.get("username")
            old_password = request.data.get("old_password")
            user = User.objects.filter(username=username).first()
            if user:
                if user.check_password(old_password):
                    return self.check_password(request, user)
            self.result["status_code"] = '3'
            self.result["msg"] = "用户名或者密码错误，请检查！"
            return Response(self.result, status=403)
