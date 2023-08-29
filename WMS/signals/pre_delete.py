from django.dispatch import receiver
from django.db.models.signals import pre_delete
# from health.models import Product2Rs, Product2Project, Product, Project, RsInfo


# @receiver(pre_delete, sender=Project)
# def project_deleted(sender, instance, using, **kwargs):
#     """
#     删除项目记录同步删除中间表
#
#     :param sender:
#     :param instance:
#     :param kwargs:
#     :return:
#     """
#     Product2Project.objects.filter(project=instance).delete()
