from pathlib import Path
import pandas as pd

from tqdm import tqdm
from datetime import datetime, time

import pandas as pd
from django.core.management.base import BaseCommand
from project.station import models
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **options):
        run()


def run():
    arquivo_csv = "VilaMariana04-01-24-15-05-2024.csv"
    caminho_dados = Path(__file__).resolve(
    ).parent.parent.parent / 'dados' / arquivo_csv

    print(caminho_dados)
    with open(caminho_dados) as arquivo_csv:
        historical_data = pd.read_csv(arquivo_csv, sep=';', encoding='utf-8')

    total_linhas = len(historical_data)
    for linha in tqdm(historical_data.values, total=total_linhas):

        data = datetime.strptime(linha[0], '%d/%m/%Y').date()
        hora_str_padded = str(linha[1]).zfill(4)
        hora = time(int(hora_str_padded[:2]), int(hora_str_padded[2:]))
        dt_sensing = datetime.combine(data, hora)

        temperatura_replace = str(linha[2]).replace(',', '.')
        temperatura = float(temperatura_replace)

        temperatura_max_replace = str(linha[3]).replace(',', '.')
        temperatura_max = float(temperatura_max_replace)

        temperatura_min_replace = str(linha[4]).replace(',', '.')
        temperatura_min = float(temperatura_min_replace)

        umidade_replace = str(linha[5]).replace(',', '.')
        umidade = float(umidade_replace)

        pressao_replace = str(linha[11]).replace(',', '.')
        pressao = float(pressao_replace)

        velocidade_vento_replace = str(linha[14]).replace(',', '.')
        velocidade_vento = float(velocidade_vento_replace)

        direcao_vento_replace = str(linha[15]).replace(',', '.')
        direcao_vento = float(direcao_vento_replace)

        chuva_replace = str(linha[18]).replace(',', '.')
        chuva = float(chuva_replace)

        models.HistoryForecast.objects.get_or_create(
            dt_sensing = dt_sensing,
            defaults= dict(
            temperatura = temperatura,
            temperatura_maxima = temperatura_max,
            temperatura_minima = temperatura_min,
            umidade = umidade,
            pressao = pressao,
            velocidade_vento = velocidade_vento,
            direcao_vento = direcao_vento,
            chuva = chuva)
        )
