from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models.user import User
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """
    监听用户创建，创建之后自动分配物料申请人组

    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        group = Group.objects.filter(name="物料申请人").first()
        if group:
            instance.groups.add(group)
            instance.save()
