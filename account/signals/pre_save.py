# from django.dispatch import receiver
# from django.db.models.signals import pre_save
# from account.models.user import User
# from django.contrib.auth.models import Group
#
#
# @receiver(pre_save, sender=User)
# def user_created(sender, instance, **kwargs):
#     """
#     监听用户创建，创建之后自动分配物料申请人组
#
#     :param sender:
#     :param instance:
#     :param kwargs:
#     :return:
#     """
#     old_instance = User.objects.filter(id=instance.id).first()
#     if not old_instance:
#         group = Group.objects.filter(name="物料申请人").first()
#         if group:
#             instance.groups.add(group)
