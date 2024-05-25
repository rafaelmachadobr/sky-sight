"""
Módulo contendo funções utilitárias para processamento de dados meteorológicos.
"""
import pickle
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import numpy as np
import requests

from .config_file import config


def unix_to_date(unix_timestamp: int) -> tuple:
    """
    Converte um timestamp UNIX em uma tupla representando a data e hora UTC.

    Args:
        unix_timestamp (int): Timestamp UNIX a ser convertido.

    Returns:
        tuple: Tupla contendo (dia, mês, ano, hora) da data e hora correspondentes ao timestamp.
    """
    data = datetime.utcfromtimestamp(unix_timestamp)

    day = data.day
    month = data.month
    year = data.year
    hour = data.hour

    return day, month, year, hour


def __parse_forecast_data(forecast: dict) -> tuple:
    """
    Extrai os dados relevantes de uma previsão meteorológica.

    Args:
        forecast (dict): Dicionário contendo os dados de uma previsão.

    Returns:
        tuple: Tupla contendo os dados meteorológicos.
    """
    timestamp_unix = forecast["dt"]
    humidity = forecast["main"]["humidity"]
    pressure = forecast["main"]["pressure"]
    wind_speed = forecast["wind"]["speed"]
    wind_direction = forecast["wind"]["deg"]

    day, month, year, hour = unix_to_date(timestamp_unix)

    return humidity, pressure, wind_speed, wind_direction, day, month, year, hour


def __get_weather_data(latitude: float, longitude: float) -> tuple:
    """
    Obtém os dados meteorológicos para uma determinada localização.

    Args:
        latitude (float): Latitude da localização.
        longitude (float): Longitude da localização.

    Returns:
        tuple: Tupla contendo os dados meteorológicos e o nome da cidade.
    """
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
    forecast_list = data["list"]

    city_name = data["city"]["name"]
    city_country = data["city"]["country"]

    weather = forecast_list[0]["weather"][0]["main"]
    weather_description = forecast_list[0]["weather"][0]["description"]

    weather_data = [__parse_forecast_data(forecast)
                    for forecast in forecast_list]
    return weather_data, city_name, city_country, weather, weather_description


def import_model(model_name: str) -> object:
    """
    Importa um modelo de previsão de temperatura.

    Args:
        model_name (str): Nome do arquivo contendo o modelo.

    Returns:
        object: Objeto do modelo importado.
    """
    with open(
            Path(__file__).resolve().parent.parent /
        f'station/modelos/{model_name}', 'rb'
    ) as file:
        model = pickle.load(file)

    return model


def __get_condition_tip(temperature: int) -> tuple:
    """
    Retorna a condição climática baseada na temperatura.

    Args:
        temperature (int): Temperatura atual.

    Returns:
        tuple: Tupla contendo a condição climática e uma dica associada.
    """
    # Verificando a temperatura para determinar a condição climática
    if temperature < 20:
        return "Frio", "Use roupas quentes e aproveite uma xícara de chocolate quente!"

    # Retorna 'Agradável' se a temperatura estiver entre os limites agradável e quente
    if temperature < 40:
        return "Agradável", "Aproveite o clima agradável para um passeio ao ar livre."

    # Se a temperatura for maior ou igual a 40, é considerado quente
    return "Quente", "Mantenha-se fresco e hidratado durante o dia."


def __weather_alert(temperature: int) -> Tuple[str, List[str]]:
    """
    Fornece um alerta climático com base na temperatura e umidade.

    Args:
        temperature (int): Temperatura atual.

    Returns:
        Tuple[str, List[str]]: Título e lista de alertas climáticos.
    """
    title = ""
    alerts = []

    if temperature > 30:
        title = "Proteja-se do Sol e do Calor:"
        alerts.extend([
            "Evite a exposição direta ao sol das 10h às 16h.",
            "Use protetor solar para evitar queimaduras solares e danos à pele.",
            "Utilize chapéus e óculos escuros, principalmente se tiver pele clara.",
            "Proteja as crianças com chapéus de abas e roupas leves.",
            "Vista roupas leves e que não retenham calor.",
            "Diminua os esforços físicos e descanse frequentemente em locais com sombra fresca.",
            "Em veículos sem ar-condicionado, mantenha as janelas abertas para a ventilação.",
            "Nunca deixe crianças e animais dentro de veículos estacionados, " +
            "mesmo que por curto período."
        ])
    if temperature >= 25:
        title = "Hidratação é fundamental:"
        alerts.extend([
            "Aumente a ingestão de água ou de sucos de frutas naturais, sem adição de açúcar.",
            "Evite bebidas alcoólicas e com elevado teor de açúcar.",
            "Faça refeições leves, pouco condimentadas e mais frequentes.",
            "Recém-nascidos, crianças, idosos e pessoas doentes podem não sentir sede. " +
            "Ofereça água sempre."
        ])

    return (title, alerts) if alerts else ("", [])


def __get_model_input(data: tuple, mean_pressure_inst: int) -> list:
    """
    Cria a entrada do modelo com os dados meteorológicos.

    Args:
        data (tuple): Tupla contendo os dados meteorológicos.
        mean_pressure_inst (int): Pressão média instantânea.

    Returns:
        list: Lista contendo a entrada do modelo.
    """
    humidity, _, wind_speed, wind_direction, day, month, year, hour = data
    return [[humidity, mean_pressure_inst, wind_speed, wind_direction, day, month, year, hour]]


def __get_formatted_date(data: tuple) -> str:
    """
    Formata a data e hora dos dados meteorológicos.

    Args:
        data (tuple): Tupla contendo os dados meteorológicos.

    Returns:
        str: Data e hora formatadas.
    """
    _, _, _, _, day, month, year, hour = data
    data_time = datetime(year, month, day, hour)
    return data_time.strftime("%Y-%m-%d %H:%M:%S")


def __get_period_of_day(hour: int) -> str:
    """
    Retorna o período do dia baseado na hora.

    Args:
        hour (int): Hora do dia.

    Returns:
        str: Período do dia.
    """

    if 6 <= hour < 18:
        return "d"

    return "n"


def __process_weather_data(
        data: tuple, model, mean_pressure_inst: int, city_name: str,
        city_country: str, weather: str, weather_description: str,
        latitude: float, longitude: float
) -> dict:
    """
    Processa os dados meteorológicos e retorna as previsões de temperatura.

    Args:
        data (tuple): Tupla contendo os dados meteorológicos.
        model (object): Objeto do modelo de previsão.
        mean_pressure_inst (int): Pressão média instantânea.

    Returns:
        dict: Dicionário contendo as previsões de temperatura.
    """
    model_input = __get_model_input(data, mean_pressure_inst)
    prediction_max, prediction_min, prediction = model.predict(model_input)[0]
    formatted_date = __get_formatted_date(data)
    condition, tip = __get_condition_tip(prediction)
    title, alerts = __weather_alert(data[0])  # humidity
    period_of_day = __get_period_of_day(data[-1])

    return {
        "informacoes_climaticas": {
            "temperatura_maxima": prediction_max,
            "temperatura_minima": prediction_min,
            "temperatura": prediction,
            "humidade": data[0],
            "pressao": data[1],
        },
        "vento": {
            "velocidade_vento": data[2],
            "direcao_vento": data[3]
        },
        "condicao_climatica": condition,
        "dica": tip,
        "alerta": {
            "titulo": title if title else "Sem alertas",
            "conteudo": alerts,
        },
        "data": formatted_date,
        "cidade": {
            "nome": city_name,
            "cordenadas": {
                "latitude": latitude,
                "longitude": longitude
            },
            "codigo_pais": city_country
        },
        "clima": {
            "condicao": weather,
            "descricao": weather_description
        },
        "periodo_do_dia": period_of_day
    }


def get_temperature_predictions(latitude: float, longitude: float, model: object) -> list:
    """
    Obtém previsões de temperatura para uma determinada localização.

    Args:
        latitude (float): Latitude da localização.
        longitude (float): Longitude da localização.
        model (object): Objeto do modelo de previsão.

    Returns:
        list: Lista de previsões de temperatura.
    """
    weather_data, city_name, city_country, weather, weather_description = __get_weather_data(
        latitude, longitude)
    mean_pressure_inst = 930
    predictions = []

    for data in weather_data:
        prediction_data = __process_weather_data(
            data, model, mean_pressure_inst, city_name, city_country, weather, weather_description, latitude, longitude)
        predictions.append(prediction_data)

    return predictions


def remove_nan_samples(X, y):
    # Converter para numpy arrays
    X = np.array(X)
    y = np.array(y)

    # Identificar índices das amostras com valores NaN nas variáveis de entrada
    nan_indices = np.any(np.isnan(X), axis=1)

    # Remover amostras com valores NaN tanto de X quanto de y
    X_cleaned = X[~nan_indices]
    y_cleaned = y[~nan_indices]

    return X_cleaned, y_cleaned
