from django.conf import settings
from django.urls import URLPattern, URLResolver
import os
import sys
import django
import pandas as pd
import datetime

sys.path.append("../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenWMS.settings")
django.setup()
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.urls import URLPattern, URLResolver


def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern), l.name]
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
    yield from list_urls(lis[1:], acc)


class Command(BaseCommand):
    help = 'List all URLs from the urlconf'

    def handle(self, *args, **options):

        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

        records, glen, nlen = [], 0, 0

        for p in list_urls(urlconf.urlpatterns):
            record = [''.join(p[:2]), p[2]]

            # Update me, or add an argument
            if record[0].startswith('yourapp'):

                clen = len(record[0])
                if clen > glen: glen = clen

                clen = len(record[1])
                if clen > nlen: nlen = clen

                records.append(record)

        print('{:-<{width}}'.format('', width=glen + nlen))
        print('{:<{glen}}Name'.format('Path', glen=glen + 4))
        print('{:-<{width}}'.format('', width=glen + nlen))
        for record in records:
            print('{path:<{glen}}{name}'.format(path=record[0],
                                                name=record[1],
                                                glen=glen + 4))
        print('{:-<{width}}'.format('', width=glen + nlen))


if __name__ == '__main__':
    c = Command()
    c.handle()
