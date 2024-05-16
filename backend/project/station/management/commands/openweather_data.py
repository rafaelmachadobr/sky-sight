import json
import requests

from tqdm import tqdm
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from project.station import models, utils

from project.station.config_file import config

class Command(BaseCommand):
    def handle(self, *args, **options):
        run()


def run():

    url = f'https://api.openweathermap.org/data/2.5/weather?lat=-23.587&lon=-46.655&units=metric&appid={config["OPENWEATHERMAP_API_KEY"]}'
    open_weather_data = json.loads(requests.get(url).text)

    data_unix = open_weather_data['dt']
    unix_to_date = utils.unix_to_date(data_unix)

    dt_sensing = datetime(unix_to_date[2], unix_to_date[1], unix_to_date[0], unix_to_date[3]) 
    dt_sensing -= timedelta(hours=3)

    temperatura = open_weather_data['main']['temp']
    temperatura_minima = open_weather_data['main']['temp_min']
    temperatura_maxima = open_weather_data['main']['temp_max']
    pressao = open_weather_data['main']['pressure']
    umidade = open_weather_data['main']['humidity']
    velocidade_vento = open_weather_data['wind']['speed']
    direcao_vento = open_weather_data['wind']['deg']

    if 'rain' in open_weather_data:
        chuva = open_weather_data['rain']['1h']
    else:
        chuva = 0


    try:
        models.HistoryForecast.objects.get(dt_sensing=dt_sensing)
        print(models.HistoryForecast.objects.get(dt_sensing=dt_sensing))
        print('already exists in the database:', dt_sensing)
    except models.HistoryForecast.DoesNotExist:
        models.HistoryForecast.objects.get_or_create(
            dt_sensing = dt_sensing,
            defaults= dict(
            temperatura = temperatura,
            temperatura_maxima = temperatura_maxima,
            temperatura_minima = temperatura_minima,
            umidade = umidade,
            pressao = pressao,
            velocidade_vento = velocidade_vento,
            direcao_vento = direcao_vento,
            chuva = chuva)
        )
        print('dt_sensing created:', dt_sensing)