from django.core.management.base import BaseCommand

from project.station import models

class Command(BaseCommand):
    def handle(self, *args, **options):
        run()


def run():
    teste = models.HistoryForecast.objects.filter().all()
    print(teste)