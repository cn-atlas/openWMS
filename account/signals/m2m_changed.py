import json
import datetime
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

# @receiver(m2m_changed, sender=Report.other_report_file.through)
# def report_other_changed(sender, instance, action, pk_set, *args, **kwargs):
#     update_report(instance, action)
