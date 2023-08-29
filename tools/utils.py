import re
import pytz
import random
import logging
import hashlib
import pandas as pd
from uuid import uuid4
# from lxml import etree as et
from decimal import Decimal
from django.conf import settings
from datetime import datetime
from django.utils.timezone import localtime
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from django.core.files.storage import default_storage

# logger 实例化，希望所有 logger 都直接导入这个，不建议使用 print
logger = logging.getLogger(__name__)
try:
    from io import BytesIO as IO  # for modern python
except ImportError:
    from io import StringIO as IO  # for legacy python


def get_date_time_now_local():
    """
    统一返回本地时间（上海）
    """
    return datetime.now(pytz.timezone(settings.TIME_ZONE))


def get_local_time(value, is_date=False):
    """
    统一返回不带时区格式的本地时间 (上海)
    注：加这个函数的目的是，在使用pandas生成表格时，pandas不支持timezone格式的时间
    """
    from django.utils import timezone
    if value is not None:
        local_time = timezone.localtime(value)
        if not is_date:
            return local_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return local_time.strftime('%Y-%m-%d')
    else:
        return None


# def get_site_url(request):
#     http = request.build_absolute_uri(None)
#     return "/".join(http.split("/")[:3])


# def calculate_file_md5(file_path):
#     with open(file_path, 'rb') as f:
#         hasher = hashlib.md5()
#         while chunk := f.read(4096):
#             hasher.update(chunk)
#     return hasher.hexdigest()


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso", ".tif",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
    ]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def generate_random_char(length=2):
    text = ''.join(random.sample(
        ['Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', 'I', 'H', 'G', 'F', 'E',
         'D', 'C', 'B', 'A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
         'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'], length))
    return text


def generate_order_number(user_id, order_id):
    """
    生成订单号
    生成规则: 当前下单时间+用户id后四位+订单id后四位+随机字符串2位
    """
    base_code = datetime.now().strftime('%Y%m%d%H%M%S')
    random_char = generate_random_char()
    user_id = str(user_id)
    order_id = str(order_id)
    order_number = base_code[-12:] + user_id[-4:].zfill(4) + order_id[-4:] + random_char
    return order_number


def generate_pedigree_number():
    """
    生成家系编号
    生成规则: 当前下单时间+随机字符串2位
    """
    base_code = datetime.now().strftime('PD%Y%m%d%H%M%S')
    random_char = generate_random_char()
    pedigree_number = base_code + random_char
    return pedigree_number


def get_current_protocol_host_port(request):
    """
    由于uwsgi的存在，protocol 好像经常会返回 false
    :param request:
    :return:
    """
    # 测试的时候使用穿透，不是 nginx 代理的，无法获取到是不是https，但是支付一定要用https，所以如此设置
    if settings.DEBUG:
        current_url = "{}s://{}".format(request.scheme, get_current_site(request))
    else:
        current_url = "{}://{}".format(request.scheme, get_current_site(request))
    return current_url


def generate_user_token(user):
    """
    生成用户登陆的 API TOKEN
    """
    user = authenticate(username=user.username)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


def delete_spaces(str):
    """
    删除字符串两边的空格
    """
    if str is not None:
        return str.strip()
    return None


def is_datetime(datatime):
    try:
        if pd.isnull(datatime):
            return False
        pd.to_datetime(datatime, format='%Y-%m-%d', errors='raise')  # 这边datetime如果是个nan类型，也会返回true
        return True
    except ValueError:
        return False


def cncurrency(value, capital=True, prefix=False, classical=None):
    """
    人民币数字转大写汉字
    """
    '''
    参数:
    capital:    True   大写汉字金额
                False  一般汉字金额
    classical:  True   元
                False  圆
    prefix:     True   以'人民币'开头
                False, 无开头
    '''
    if not isinstance(value, (Decimal, str, int)):
        msg = '''
        由于浮点数精度问题，请考虑使用字符串，或者 decimal.Decimal 类。
        因使用浮点数造成误差而带来的可能风险和损失作者概不负责。
        '''
        # warnings.warn(msg, UserWarning)
    # 默认大写金额用圆，一般汉字金额用元
    if classical is None:
        classical = True if capital else False

    # 汉字金额前缀
    if prefix is True:
        prefix = '人民币'
    else:
        prefix = ''

    # 汉字金额字符定义
    dunit = ('角', '分')
    if capital:
        num = ('零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖')
        iunit = [None, '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿', '拾', '佰', '仟', '万', '拾', '佰', '仟']
    else:
        num = ('〇', '一', '二', '三', '四', '五', '六', '七', '八', '九')
        iunit = [None, '十', '百', '千', '万', '十', '百', '千', '亿', '十', '百', '千', '万', '十', '百', '千']
    if classical:
        iunit[0] = '元' if classical else '圆'
    # 转换为Decimal，并截断多余小数

    if not isinstance(value, Decimal):
        value = Decimal(value).quantize(Decimal('0.01'))

    # 处理负数
    if value < 0:
        prefix += '负'  # 输出前缀，加负
        value = - value  # 取正数部分，无须过多考虑正负数舍入
        # assert - value + value == 0
    # 转化为字符串
    s = str(value)
    if len(s) > 19:
        raise ValueError('金额太大了，不知道该怎么表达。')
    istr, dstr = s.split('.')  # 小数部分和整数部分分别处理
    istr = istr[::-1]  # 翻转整数部分字符串
    so = []  # 用于记录转换结果

    # 零
    if value == 0:
        return prefix + num[0] + iunit[0]
    haszero = False  # 用于标记零的使用
    if dstr == '00':
        haszero = True  # 如果无小数部分，则标记加过零，避免出现“圆零整”

    # 处理小数部分
    # 分
    if dstr[1] != '0':
        so.append(dunit[1])
        so.append(num[int(dstr[1])])
    else:
        so.append('整')  # 无分，则加“整”
    # 角
    if dstr[0] != '0':
        so.append(dunit[0])
        so.append(num[int(dstr[0])])
    elif dstr[1] != '0':
        so.append(num[0])  # 无角有分，添加“零”
        haszero = True  # 标记加过零了

    # 无整数部分
    if istr == '0':
        if haszero:  # 既然无整数部分，那么去掉角位置上的零
            so.pop()
        so.append(prefix)  # 加前缀
        so.reverse()  # 翻转
        return ''.join(so)

    # 处理整数部分
    for i, n in enumerate(istr):
        n = int(n)
        if i % 4 == 0:  # 在圆、万、亿等位上，即使是零，也必须有单位
            if i == 8 and so[-1] == iunit[4]:  # 亿和万之间全部为零的情况
                so.pop()  # 去掉万
            so.append(iunit[i])
            if n == 0:  # 处理这些位上为零的情况
                if not haszero:  # 如果以前没有加过零
                    so.insert(-1, num[0])  # 则在单位后面加零
                    haszero = True  # 标记加过零了
            else:  # 处理不为零的情况
                so.append(num[n])
                haszero = False  # 重新开始标记加零的情况
        else:  # 在其他位置上
            if n != 0:  # 不为零的情况
                so.append(iunit[i])
                so.append(num[n])
                haszero = False  # 重新开始标记加零的情况
            else:  # 处理为零的情况
                if not haszero:  # 如果以前没有加过零
                    so.append(num[0])
                    haszero = True

    # 最终结果
    so.append(prefix)
    so.reverse()
    return ''.join(so)


def is_weekend(date):
    print(date)
    date_list = date.split('-')
    y = int(date_list[0])
    m = int(date_list[1])
    d = int(date_list[2])
    d = datetime(y, m, d)
    if d.weekday() > 4:
        return True
    else:
        return False


def generate_excel_file(user, file_name, pd_data_frame):
    from health.models.attachment import CommonFile
    file_uuid = uuid4()
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    new_file_name = '{}_{}'.format(file_name, current_time) + '.xlsx'
    excel_file = IO()
    writer = pd.ExcelWriter(excel_file)

    for item in pd_data_frame:
        item.get('sheet_data_frame').to_excel(writer, float_format='%.5f', index=False, engine='openpyxl',
                                              sheet_name=item.get('sheet_name', 'sheet'))
    # writer.save() # wps打开一切正常，但是在微软Excel打开时，会提示xxx.xlsx中的部分内容有问题，是否让我们尽量尝试修复？
    # 把writer.save()方法关闭后就解决了这个问题，通过对比开启前和开启后文件大小来看，开启后的大小多了一倍
    # 原因可能是导出结果之后关于保存的部分写重复了
    writer.close()
    excel_file.seek(0)

    file = default_storage.save(
        'common_files/export_files/{}/{}'.format(datetime.today().year,
                                                 datetime.today().month) + '/' + new_file_name,
        excel_file)
    obj = CommonFile(is_show=True,
                     name=file_name,
                     type='csv',
                     remark=file_name,
                     file=file,
                     uuid=file_uuid,
                     creator=user,
                     editor=user
                     )
    obj.save()
    return obj


# def decodeXMLData(xml_data):
#     try:
#         # 解析xml数据
#         xml = str(xml_data, encoding="utf-8")
#         print("xml", xml)
#         return_dict = {}
#         tree = et.fromstring(xml)
#         # xml 解析
#         return tree
#     except Exception as e:
#         return False


def get_role_info(instance):
    """
    判断是销售还是客户，销售: seller; 客户: customer; 员工: employee; 其他: other

    :param instance:
    :return:
    """
    if instance.is_superuser:
        return "admin"
    elif not isinstance(instance.user_customers.first(), type(None)):
        return "customer"
    elif instance.company:
        if -1 != instance.company.name.find("<企业名称>"):
            if instance.department:
                if instance.department.department_name.find("财务") > -1:
                    return "finance"
                if instance.department.department_name.find("商务") > -1:
                    return "commerce"
                if instance.department.department_name.find("质量") > -1:
                    return "quality"
                if not isinstance(instance.user_seller.first(), type(None)):
                    return "seller"
            return "employee"
    elif not isinstance(instance.user_seller.first(), type(None)):
        return "seller"
    return "other"


def special_char_replace(string):
    """
    对字符串进行中文字符替换处理
    """
    punc1 = "[\uff0c]"  # 中文逗号unicode编码
    punc2 = '[\uff1a]'  # 中文冒号unicode编码
    string = re.sub(punc1, ",", string)
    string = re.sub(punc2, ":", string)

    return string


def get_match_text(string, type=None):
    """
    使用正则表达式匹配文本，并返回
    """
    rst = None
    if type == 'product_number':
        pattern = r'ZKP-[a-zA-Z]*-[\d]*'
        matchObj = re.match(pattern, string)
        rst = matchObj.group().strip() if matchObj else None

    return rst


def file_encrypt(file_stream: str, algorithm='md5') -> str:
    """
    传入文件流对文件进行加密计算
    """
    return hashlib.new(algorithm, file_stream).hexdigest()


def alarm_check(rule, number):
    """
    告警检查，用于对lims实验结果参数的数据进行检查
    """
    number = float(number)
    var_way = rule.get('var_way')
    float_min_var = rule.get('float_min_var')
    float_max_var = rule.get('float_max_var')

    alarm_code = 0
    if rule.get('alarm_type') == 'alarm':
        alarm_code = 1
    elif rule.get('alarm_type') == 'reject':
        alarm_code = -1

    if var_way == '等于阈值警告':
        if number == float_min_var or number == float_max_var:
            return alarm_code
    elif var_way == '不等于阈值警告':
        if number != float_min_var or number != float_max_var:
            return alarm_code
    elif var_way == '大于阈值警告':
        if number > float_max_var:
            return alarm_code
    elif var_way == '小于阈值警告':
        if number < float_min_var:
            return alarm_code
    elif var_way == '区间内警告(不含边界)':
        if float_min_var < number < float_max_var:
            return alarm_code
    elif var_way == '区间内警告(含边界)':
        if float_min_var <= number <= float_max_var:
            return alarm_code
    elif var_way == '区间内警告(前开后闭)':
        if float_min_var < number <= float_max_var:
            return alarm_code
    elif var_way == '区间内警告(前闭后开)':
        if float_min_var <= number < float_max_var:
            return alarm_code
    elif var_way == '区间外警告(不含边界)':
        if number < float_min_var or number > float_max_var:
            return alarm_code
    elif var_way == '区间外警告(含边界)':
        if number <= float_min_var or number >= float_max_var:
            return alarm_code
    elif var_way == '区间外警告(前开后闭)':
        pass
    elif var_way == '区间外警告(前闭后开)':
        pass
    else:
        return 0


class MyDict(dict):
    # 一个类里面只能有一个init方法<br>
    # #self.__dict__方法就是<br>用来显示类里面的属性的（函数也是类的一种属性）
    def __init__(self, **kwargs):
        super(MyDict, self).__init__(kwargs)
        self.__dict__ = self
