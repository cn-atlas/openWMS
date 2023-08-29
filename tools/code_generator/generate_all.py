import os
import sys
import django

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenWMS.settings")
django.setup()

from tools.code_generator.filters import do_generate_filters
from tools.code_generator.serializers import do_generate_serializers
from tools.code_generator.views import do_generate_viewsets

if __name__ == '__main__':
    do_generate_filters()
    do_generate_serializers()
    do_generate_viewsets()
