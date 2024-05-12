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
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": config["OPENWEATHERMAP_API_KEY"],
        "lang": "pt_br",
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    lista_previsoes = data["list"]

    dados_meteorologicos = []
    for previsao in lista_previsoes:
        timestamp_unix = previsao["dt"]
        umidade_instantanea = previsao["main"]["humidity"]
        pressao_instantanea = previsao["main"]["pressure"]
        velocidade_vento = previsao["wind"]["speed"]
        direcao_vento = previsao["wind"]["deg"]
        dia, mes, ano, hora = unix_para_data(timestamp_unix)
        dados_meteorologicos.append(
            (umidade_instantanea, pressao_instantanea, velocidade_vento, direcao_vento, dia, mes, ano, hora))

    return dados_meteorologicos


def importar_modelo(nome_modelo: str):
    BASE_DIR = Path(__file__).resolve().parent.parent

    with open(BASE_DIR / f'station/modelos/{nome_modelo}', 'rb') as file:
        modelo = pickle.load(file)

    return modelo


def __obter_condicao_dica(temperatura: int):
    """Retorna a condição climática baseada na temperatura."""
    # Verificando a temperatura para determinar a condição climática
    if temperatura < 20:
        return "Frio", "Use roupas quentes e aproveite uma xícara de chocolate quente!"
    elif temperatura < 40:
        # Retorna 'Agradável' se a temperatura estiver entre os limites agradável e quente
        return "Agradável", "Aproveite o clima agradável para um passeio ao ar livre."
    else:
        return "Quente", "Mantenha-se fresco e hidratado durante o dia."


def __alerta_climatico(temperatura):
    """Fornece um alerta climático com base na temperatura e umidade."""
    if temperatura > 30:
        return "Alerta de calor: temperatura muito alta!"
    elif temperatura > 80:
        return "Alerta de umidade: risco de chuvas intensas!"
    else:
        return "Sem alertas no momento."


def obter_previsoes_temperatura(latitude, longitude, modelo):
    dados_meteorologicos = obter_dados_meteorologicos(latitude, longitude)
    media_pressao_inst = 930
    previsoes = []

    for dado in dados_meteorologicos:
        (umidade_instantanea, pressao_instantanea, velocidade_vento,
         direcao_vento, dia, mes, ano, hora) = dado

        entrada_modelo = [[umidade_instantanea, media_pressao_inst, velocidade_vento,
                          direcao_vento, dia, mes, ano, hora]]

        previsao = modelo.predict(entrada_modelo)[0]

        data_hora = datetime(ano, mes, dia, hora)
        data_formatada = data_hora.strftime("%Y-%m-%d %H:%M:%S")

        condicao_climatica, dica = __obter_condicao_dica(previsao)

        alerta = __alerta_climatico(umidade_instantanea)

        previsoes.append({
            "temperatura": previsao,
            "temperatura_arredondada": round(previsao),
            "humidade": umidade_instantanea,
            "pressao": pressao_instantanea,
            "velocidade_vento": velocidade_vento,
            "direcao_vento": direcao_vento,
            "condicao_climatica": condicao_climatica,
            "dica": dica,
            "alerta": alerta,
            "data": data_formatada
        })

    return previsoes
