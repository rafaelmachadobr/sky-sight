import pickle
from datetime import datetime
from pathlib import Path

import requests

from .config_file import config


def unix_para_data(unix_timestamp):
    data = datetime.utcfromtimestamp(unix_timestamp)

    dia = data.day
    mes = data.month
    ano = data.year
    hora = data.hour

    return dia, mes, ano, hora


def obter_dados_meteorologicos(latitude, longitude):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": config["OPENWEATHERMAP_API_KEY"],
        "lang": "pt_br",
        "units": "metric"
    }

    response = requests.get(url, params=params)

    data = response.json()

    umidade_instantanea = data["main"]["humidity"]
    pressao_instantanea = data["main"]["pressure"]
    velocidade_vento = data["wind"]["speed"]
    direcao_vento = data["wind"]["deg"]
    timestamp_unix = data["dt"]

    dia, mes, ano, hora = unix_para_data(timestamp_unix)

    return umidade_instantanea, pressao_instantanea, velocidade_vento, direcao_vento, dia, mes, ano, hora


def importar_modelo(nome_modelo: str):
    BASE_DIR = Path(__file__).resolve().parent.parent

    with open(BASE_DIR / f'station/modelos/{nome_modelo}', 'rb') as file:
        modelo = pickle.load(file)

    return modelo
