from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from account.models import Department, User
from itertools import chain
from functools import reduce
import operator
from django.contrib.auth.models import Group
from WMS.models.inventory import WmsInventory
from WMS.models.item import WmsItem, WmsItemType


def users_in_my_charge(user) -> list:
    users = [user]
    if user.is_director:
        user_department = Department.objects.filter(department_users=user).first()
        if user_department:
            user_department = user_department.get_leafnodes(include_self=True)
        users = User.objects.filter(department__in=user_department)
    return users


def get_creators_in_my_charge(user) -> list:
    return users_in_my_charge(user)


def get_group_names(request_user) -> list:
    # 获取该用户涉及的所有组（部门组和个人组）
    groups = request_user.groups.all()
    user_depart = request_user.department
    if user_depart:
        depart_groups = Group.objects.filter(depart_groups__department_users=request_user).all()
        groups = list(set(chain(groups, depart_groups.all())))
    print(groups)
    obj_range_group_name = [group.name for group in groups]
    print(obj_range_group_name)
    return obj_range_group_name


def get_qs_in_permission(qs, request_user):
    if isinstance(request_user, AnonymousUser):
        # 不允许匿名用户查询
        return qs.filter(creator__id=-1)

    if request_user.is_superuser:
        return qs

    my_self_qs = qs.filter(Q(creator=request_user) | Q(editor=request_user))
    obj_range_group_name = get_group_names(request_user)

    # 没有记录或者没有其他权限仅返回我创建的，而且框架层判断会要求必须有 model 权限
    if not obj_range_group_name:
        return my_self_qs

    # 超级管理员、仓库管理员、管理员具有所有查询权限，但是具体界面或者接口有没有权限通过权限表决定
    if "仓库管理员" in obj_range_group_name \
            or "管理员" in obj_range_group_name:
        return qs
    elif "物料申请人" in obj_range_group_name:
        if qs.model in [WmsInventory, WmsItemType, WmsItem]:
            return qs
    # 部门支持，先不管
    # elif "物料申请人" in obj_range_group_name:
    #     # 销售
    #     # print(object_permission.name)
    #     # print(time.time())
    #     # print(qs)
    #     if qs.model.get_order_about_me_query_filter() or qs.model == Order:
    #         users_in_my_charger = get_creators_in_my_charge(request_user)
    #         # 客户要绑定销售才查得到
    #         cs_filter = "customer__seller__user__in"
    #         cs_filter_dic = {
    #             "__".join([qs.model.get_order_about_me_query_filter(),
    #                        cs_filter]) if not qs.model == Order else cs_filter: users_in_my_charger}
    #         # 销售不绑定帐号查不到
    #         s_filter = "seller__user__in"
    #         s_filter_dic = {
    #             "__".join([qs.model.get_order_about_me_query_filter(),
    #                        s_filter]) if not qs.model == Order else s_filter: users_in_my_charger}
    #         # print(cs_filter_dic, s_filter_dic)
    #         q_filters.append(cs_filter_dic)
    #         q_filters.append(s_filter_dic)
    # else:
    return my_self_qs


class ObjectRangeQSFilterMixin:

    @property
    def qs(self):
        """
        权限范围

        * 如果是管理员 返回全部数据

        * 如果是匿名用户，不返回任何数据

        * 其他用户根据范围配置进行筛选 部门里面如果为空，则默认是我所管辖的所有样本，

        :return:
        """
        qs = super().qs
        request_user = getattr(self.request, 'user', None)
        return get_qs_in_permission(qs, request_user)
