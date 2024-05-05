import os
from datetime import datetime

import pandas as pd
from django.core.management.base import BaseCommand
from project.station import models

class Command(BaseCommand):
    def handle(self, *args, **options):
        run()


def run():
    # with open("/home/rafael/VilaMariana03-01-23-06-04-2023.csv", 'r') as arquivo_csv:
    with open("/home/rafael/VilaMariana07-04-24-04-05-2024.csv", 'r') as arquivo_csv:
        historical_data = pd.read_csv(arquivo_csv, sep=';', encoding='utf-8')

    for linha in historical_data.values:

        date= linha[0]
        data = datetime.strptime(date, "%d/%m/%Y")

        temperatura_replace = str(linha[2]).replace(',', '.')
        temperatura = float(temperatura_replace)

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

        models.HistoryForecast.objects.create(
            data = data,
            temperatura = temperatura,
            umidade = umidade,
            pressao = pressao,
            velocidade_vento = velocidade_vento,
            rajada_vento = rajada_vento,
            chuva = chuva
        )