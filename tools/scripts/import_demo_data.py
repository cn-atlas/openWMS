import os
import sys
import django
import pandas as pd
import datetime

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenWMS.settings")
django.setup()

from account.models.user import User
from WMS.models.item import WmsAbsItem, WmsItem
from WMS.models.inventory import WmsInventory
from WMS.models.warehouse import WmsRack

abs_item_key_dict = {
    "物品编号": "number",
    "物品名称": "name",
    "规格": "specs",
    "型号": "model",
    "生产厂家": "manufacturer",
    "单位": "unit",
    # "期初结存": "total_number",
}

item_key_dict = {
    "物品编号": "number",
    "批号": "batch_number",
    # "生产日期": "produce_date",
    "有效日期": "expiry_date",
    "期初结存": "quantity",
}


def excel2json():
    df = pd.read_excel("/Users/qinfei/PycharmProjects/OpenWMS/tools/scripts/业务台账模版11.xlsx")
    abs_items = list()
    items = list()
    for index, row in df.iterrows():
        abs_item = dict()
        item = dict()
        for index, col_name in enumerate(df.columns):
            if col_name == "物品编号":
                v = str(row[col_name]).upper()
            else:
                v = row[col_name] if not pd.isna(row[col_name]) else None
            if col_name in abs_item_key_dict.keys():
                abs_item[abs_item_key_dict[col_name]] = v
            if col_name in item_key_dict.keys():
                item[item_key_dict[col_name]] = v
        abs_items.append(abs_item)
        items.append(item)
    return abs_items, items


if __name__ == '__main__':
    abs_items, items = excel2json()
    creator = User.objects.filter(username="zk").first()
    rack = WmsRack.objects.get(pk=1)
    for abs_item in abs_items:
        abs_item_obj, created = WmsAbsItem.objects.get_or_create(**abs_item, is_show=True, creator=creator)
        print(created, abs_item_obj)
    abs_total_number_dict = dict()
    for item in items:
        _number = item.pop("number")
        # _produce_date = item.pop("produce_date")
        _expiry_date = item.pop("expiry_date")
        _quantity = item.pop("quantity")
        # if not pd.isna(_produce_date) and _produce_date:
        #     produce_date = datetime.datetime.strptime(_produce_date, "%Y.%m.%d")
        #     item["produce_date"] = produce_date
        if not pd.isna(_expiry_date) and _expiry_date:
            expiry_date = datetime.datetime.strptime(_expiry_date, "%Y.%m.%d")
            item["expiry_date"] = expiry_date
        abs_item = WmsAbsItem.objects.filter(number=str(_number).upper()).first()
        if abs_item:
            if abs_item not in abs_total_number_dict:
                abs_total_number_dict[abs_item] = 0
            abs_total_number_dict[abs_item] += _quantity
            item["abs_item"] = abs_item
            print(item)
            item_obj, created = WmsItem.objects.get_or_create(**item, is_show=True, creator=creator)
            print(created, item_obj)
            # 创建库存
            inventory_obj, created = WmsInventory.objects.get_or_create(is_show=True, creator=creator, rack=rack,
                                                                        item=item_obj, quantity=_quantity)
        else:
            print(item)
            print("X" * 50)
    #  更新总数
    for k, v in abs_total_number_dict.items():
        abs_item = WmsAbsItem.objects.get(pk=k.id)
        abs_item.total_number = v
        abs_item.save()
