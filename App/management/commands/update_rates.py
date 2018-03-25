import json
from urllib.request import urlopen

from django.conf import settings
from django.core.management import BaseCommand

from App.models import Currency, Rate


class Command(BaseCommand):
    help = 'Update rates runs by cron once a day'

    def handle(self, *args, **options):

        openexchangerates_url = 'https://openexchangerates.org/api/latest.json?app_id={key}'.format(
            key=settings.OPENEXCHANGERATES_KEY)
        data_json = urlopen(openexchangerates_url).read()
        data = json.loads(data_json)

        base, _created = Currency.objects.update_or_create(code='USD', defaults={'name': 'US Dollar'})
        for code in settings.CURRENCY_CODES:
            target, _created = Currency.objects.update_or_create(code=code)
            rate = data['rates'][code]
            Rate.objects.update_or_create(source=base, target=target, defaults={'rate': rate})
