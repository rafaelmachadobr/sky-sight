import pandas as pd

from datetime import datetime

from django.core.management.base import BaseCommand

from project.station import models

class Command(BaseCommand):
    def handle(self, *args, **options):
        run()


def run():

    with open('/home/samaram/CodeSpace/VilaMariana03-01-23-03-01-24.csv', 'r') as arquivo_csv:
        historical_data = pd.read_csv(arquivo_csv, sep=';', encoding='utf-8')

    for linha in historical_data.values:

        date= linha[0]
        data = datetime.strptime(date, "%d/%m/%Y")

        hour= linha[1]
        hora = int(hour)

        temperatura_replace = str(linha[2]).replace(',', '.')
        temperatura = float(temperatura_replace)

        temperatura_max_replace = str(linha[3]).replace(',', '.')
        temperatura_max = float(temperatura_max_replace)

        temperatura_min_replace = str(linha[4]).replace(',', '.')
        temperatura_min = float(temperatura_min_replace)

        umidade_replace = str(linha[5]).replace(',', '.')
        umidade = float(umidade_replace)

        pressao_replace = str(linha[11]).replace(',', '.')
        pressao =  float(pressao_replace)

        velocidade_vento_replace = str(linha[14]).replace(',', '.')
        velocidade_vento =  float(velocidade_vento_replace)

        rajada_vento_replace = str(linha[16]).replace(',', '.')
        rajada_vento =  float(rajada_vento_replace)

        chuva_replace = str(linha[18]).replace(',', '.')
        chuva =  float(chuva_replace)

        models.HistoryForecast.objects.update_or_create(
            data = data,
            hora = hora,
            defaults=dict(
            temperatura = temperatura,
            temperatura_maxima = temperatura_max,
            temperatura_minima = temperatura_min,
            umidade = umidade,
            pressao = pressao,
            velocidade_vento = velocidade_vento,
            rajada_vento = rajada_vento,
            chuva = chuva)
        )