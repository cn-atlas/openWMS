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


def valid_shield(request):
    '''
    向验证码服务器请求验证结果

    :param request:
    :return: {"msg":"success","success":1,"score":100}
    '''
    data = {
        "id": settings.VAPTCHA_VID,
        "secretkey": settings.VAPTCHA_KEY,
        "scene": settings.VAPTCHA_SCENE,
        "token": request.POST.get("token", "xxx"),
        "ip": get_client_ip(request),
    }
    try:
        r = requests.post(settings.VAPTCHA_VERIFY_URL, data)
        data = json.loads(r.text)
    except:
        data = {"msg": "请求验证码服务器出错，请联系管理员或稍后重试！", "success": 0, "score": 0}
    return data
