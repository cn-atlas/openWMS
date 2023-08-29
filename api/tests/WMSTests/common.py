from WMS.models import WmsWarehouse, WmsArea, WmsRack, WmsAbsItem, WmsItem, WmsInventoryMovement, WmsInventoryCheck, \
    WmsReceiptOrder, WmsShipmentOrder


def get_link(obj):
    model_name = obj._meta.model_name.lower()
    url = f'http://testserver/api/v1/{model_name}/{obj.pk}/'
    return url


def create_warehouse():
    obj = WmsWarehouse.objects.create(is_show=True, create_time="1975-08-29 00:00:00",
                                      edit_time="2021-01-19 00:00:00", creator=None, editor=None,
                                      number="FhBno8qgyJ", name="林玉珍", remark="不是免费觉得信息个人的话应该部分.")
    return obj


def create_area():
    obj = WmsArea.objects.create(is_show=True, create_time="1943-07-22 00:00:00", edit_time="1993-03-05 00:00:00",
                                 creator=None, editor=None, number="AGm0pS1e1U", name="李玉梅",
                                 warehouse=create_warehouse(),
                                 remark="部门威望不能的人以后公司项目.")
    return obj


def create_rack():
    obj = WmsRack.objects.create(is_show=True, create_time="1996-09-05 00:00:00", edit_time="1932-06-28 00:00:00",
                                 creator=None, editor=None, area=create_area(), number="BcXaItd6jX",
                                 name="刘玉兰", remark="比较他的结果项目类别能力已经.")
    return obj


def create_abs_item():
    obj = WmsAbsItem.objects.create(is_show=True, create_time="1950-08-09 00:00:00",
                                    edit_time="1988-10-09 00:00:00", creator=None, editor=None, number="wbKmEbgXvF",
                                    name="王淑华", specs="继续威望来自查看选择建设已经.", model="来源名称开始目前决定名称.",
                                    manufacturer="论坛女人空间看到主题对于.", item_type=None, unit="只是回复可能学习文件有关提高.",
                                    quantity=9.0, total_number=52.0, remark="销售经验首页学校.")
    return obj


def create_item():
    obj = WmsItem.objects.create(is_show=True, create_time="2021-08-23 00:00:00", edit_time="1963-10-11 00:00:00",
                                 creator=None, editor=None, abs_item=create_abs_item(), batch_number="SEcRgs8wXb",
                                 produce_date="1943-07-20 00:00:00", expiry_date="1987-07-23 00:00:00",
                                 remark="数据表示安全文化地区北京市场.")
    return obj


def create_inventory_movement():
    obj = WmsInventoryMovement.objects.create(is_show=False, create_time="1943-10-02 00:00:00",
                                              edit_time="1964-06-03 00:00:00", creator=None, editor=None,
                                              is_checked=True, check_time="1983-11-21 00:00:00", check_user=None,
                                              check_note="通过专业行业推荐必须非常程序.", number="XJPVFhdhv3", source_rack=None,
                                              target_rack=None, status=18, remark="运行已经网上方式记者.")
    return obj


def create_inventory_check():
    obj = WmsInventoryCheck.objects.create(is_show=True, create_time="1997-12-06 00:00:00",
                                           edit_time="1956-12-15 00:00:00", creator=None, editor=None,
                                           is_checked=False, check_time="1941-04-06 00:00:00", check_user=None,
                                           check_note="以下提供电脑特别包括技术状态.", number="cnKD7OKM7M",
                                           inventory_check_type=86, inventory_check_status=99,
                                           inventory_check_total=71.0, warehouse=None, area=None, rack=None,
                                           attachment=None, remark="必须安全直接作为更多重要.")
    return obj


def create_receipt():
    obj = WmsReceiptOrder.objects.create(is_show=True, create_time="2012-07-24 00:00:00",
                                         edit_time="1961-10-28 00:00:00", creator=None, editor=None,
                                         number="1gG6ApUfbw", receipt_type=45, supplier=None,
                                         order_no="主题发现一样应该今天生活.", payable_amount=39.0, status=94,
                                         remark="经验特别一样阅读拥有内容其他.")
    return obj


def create_shipment():
    obj = WmsShipmentOrder.objects.create(is_show=True, create_time="1993-09-19 00:00:00",
                                          edit_time="2008-07-03 00:00:00", creator=None, editor=None,
                                          is_checked=True, check_time="1930-10-29 00:00:00", check_user=None,
                                          check_note="到了感觉功能次数.", number="7E2vNyfslj", shipment_order_type=70,
                                          order_no="有些次数主题应用对于这个国家.", to_customer="发生知道是一注册.", to_user=None,
                                          receivable_amount=46.0, status=85, remark="继续出来决定目前.")
    return obj
