import sys
import json
import requests
from django.conf import settings


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Google Captcha
def get_remote_ip():
    f = sys._getframe()
    while f:
        request = f.f_locals.get("request")
        if request:
            remote_ip = request.META.get("REMOTE_ADDR", "")
            forwarded_ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
            ip = remote_ip if not forwarded_ip else forwarded_ip
            return ip
        f = f.f_back


def valid_shield(token, remote_ip):
    '''
    向验证码服务器请求验证结果

    :param request:
    :return: {"msg":"success","success":1,"score":100}
    '''
    data = {
        "id": settings.VAPTCHA_VID,
        "secretkey": settings.VAPTCHA_KEY,
        "scene": settings.VAPTCHA_SCENE,
        "token": token,
        "ip": remote_ip,
    }
    try:
        r = requests.post(settings.VAPTCHA_VERIFY_URL, data)
        data = json.loads(r.text)
    except:
        data = {"msg": "请求验证码服务器出错，请联系管理员或稍后重试！", "success": 0, "score": 0}
    return data
