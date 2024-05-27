from datetime import datetime
from warnings import filterwarnings

import numpy as np
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

from .models import HistoryForecast
from .utils import (get_temperature_predictions, import_model,
                    remove_nan_samples)

filterwarnings('ignore')


@api_view(['GET'])
def get_historical_predict_random_forest(request):

    data_atual = datetime.now().date()

    dados_do_dia = HistoryForecast.objects.filter(dt_sensing__date=data_atual)

    if not dados_do_dia.exists():
        return Response(status=404, data={"message": "Não há dados disponíveis para o dia especificado."})

    # Extrair características e rótulos de todos os dados do dia
    X = [[data.temperatura_maxima, data.temperatura_minima, data.umidade,
          data.pressao, data.chuva, data.velocidade_vento] for data in dados_do_dia]
    y = [[data.temperatura, data.umidade, data.pressao, data.chuva,
          data.velocidade_vento] for data in dados_do_dia]  # Variáveis alvo

    # Verificar e tratar valores ausentes nas variáveis de entrada
    X, y = remove_nan_samples(X, y)

    # Verificar se restaram amostras após remover as com valores ausentes
    if len(X) == 0:
        return Response(status=400, data={"message": "Todos os dados estão ausentes."})

    # Normalizar as características, se necessário
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Inicializar e treinar o modelo Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

    # Preparar os dados de previsão para o próximo dia
    dados_previsao_proximo_dia = [[data.temperatura_maxima, data.temperatura_minima,
                                   data.umidade, data.pressao, data.chuva, data.velocidade_vento] for data in dados_do_dia]

    # Normalizar os dados de previsão para o próximo dia
    dados_previsao_proximo_dia = scaler.transform(dados_previsao_proximo_dia)

    # Fazer a previsão para todos os dados do próximo dia
    previsoes_proximo_dia = rf_model.predict(dados_previsao_proximo_dia)

    # Calcular a média da previsão de temperatura para o próximo dia
    previsao_temperatura_media = round(np.mean(previsoes_proximo_dia[:, 0]), 2)

    # Calcular os valores máximos das outras variáveis
    previsao_umidade_maxima = round(np.max(previsoes_proximo_dia[:, 1]), 2)
    previsao_pressao_maxima = round(np.max(previsoes_proximo_dia[:, 2]), 2)
    previsao_chuva_maxima = round(np.max(previsoes_proximo_dia[:, 3]), 2)
    previsao_vento_maxima = round(np.max(previsoes_proximo_dia[:, 4]), 2)

    # Previsão para temperatura máxima e mínima
    previsao_temperatura_maxima = round(np.max(previsoes_proximo_dia[:, 0]), 2)
    previsao_temperatura_minima = round(np.min(previsoes_proximo_dia[:, 0]), 2)

    # Calcular a previsão de chuva máxima em percentual (1 mm = 100%)
    previsao_chuva_maxima_percentual = round(previsao_chuva_maxima * 100, 2)

    # Converter a velocidade do vento de m/s para km/h
    previsao_vento_maxima_kmh = round(previsao_vento_maxima * 3.6, 2)

    return Response(status=200, data={
        "previsao_temperatura_media": previsao_temperatura_media,
        "previsao_temperatura_maxima": previsao_temperatura_maxima,
        "previsao_temperatura_minima": previsao_temperatura_minima,
        "previsao_umidade_maxima": previsao_umidade_maxima,
        "previsao_pressao_maxima": previsao_pressao_maxima,
        "previsao_chuva_maxima_percentual": previsao_chuva_maxima_percentual,
        "previsao_vento_maxima": previsao_vento_maxima_kmh,
    })


@api_view(['GET'])
def get_historical_predict_linear_regression_ibirapuera_park(request: Request) -> Response:
    """
    Retorna uma previsão da temperatura para o Parque Ibirapuera utilizando regressão linear.

    Args:
        request (Request): Requisição HTTP.

    Returns:
        Response: Resposta HTTP contendo a previsão da temperatura, temperatura arredondada,
        umidade, pressão, velocidade do vento, direção do vento, condição climática, dica, 
        alerta e data.

    Raises:
        Response: Se a requisição não for do tipo GET.
    """
    if request.method != "GET":
        return Response(status=405, data={"message": "Método não permitido."})

    latitude = -23.587
    longitude = -46.655

    model = import_model("modelo_regressao_linear.sav")

    predictions = get_temperature_predictions(latitude, longitude, model)

    city_name = "Ibirapuera"
    city_country = "BR"

    city = {
        "name": city_name,
        "coord": {
            "lat": latitude,
            "lon": longitude
        },
        "country": city_country
    }

    count = len(predictions)

    response_data = {
        "cod": 200,
        "cnt": count,
        "list": predictions, 
        "city": city
    }

    return Response(response_data, status=200, content_type='application/json; charset=UTF-8')
