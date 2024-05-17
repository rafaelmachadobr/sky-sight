import numpy as np

from warnings import filterwarnings
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

from .utils import get_temperature_predictions, import_model, remove_nan_samples

from . import models
filterwarnings('ignore')

@api_view(['GET'])
def get_historical_predict(request):

    data_atual = datetime.now().date()
    # data_atual = datetime.strptime("2024-05-14", "%Y-%m-%d").date()

    dados_do_dia = models.HistoryForecast.objects.filter(dt_sensing__date=data_atual)

    if not dados_do_dia.exists():
        return Response(status=404, data={"message": "Não há dados disponíveis para o dia especificado."})

    # Extrair características e rótulos de todos os dados do dia
    X = [[data.temperatura_maxima, data.temperatura_minima, data.umidade, data.pressao, data.chuva, data.velocidade_vento] for data in dados_do_dia]
    y = [[data.temperatura, data.umidade, data.pressao, data.chuva, data.velocidade_vento] for data in dados_do_dia]  # Variáveis alvo

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
    dados_previsao_proximo_dia = [[data.temperatura_maxima, data.temperatura_minima, data.umidade, data.pressao, data.chuva, data.velocidade_vento] for data in dados_do_dia]

    # Normalizar os dados de previsão para o próximo dia
    dados_previsao_proximo_dia = scaler.transform(dados_previsao_proximo_dia)

    # Fazer a previsão para todos os dados do próximo dia
    previsoes_proximo_dia = rf_model.predict(dados_previsao_proximo_dia)

    # Calcular a média das previsões para o próximo dia
    previsao_media_proximo_dia = np.mean(previsoes_proximo_dia, axis=0)
    print("Previsão média para o próximo dia:", previsao_media_proximo_dia)

    # Extrair previsões individuais
    previsao_temperatura_media = previsao_media_proximo_dia[0]
    previsao_umidade_media = previsao_media_proximo_dia[1]
    previsao_pressao_media = previsao_media_proximo_dia[2]
    previsao_chuva_media = previsao_media_proximo_dia[3]
    previsao_vento_media = previsao_media_proximo_dia[4]

    # Previsão para temperatura máxima e mínima
    previsao_temperatura_maxima = np.max(previsoes_proximo_dia[:, 0])
    previsao_temperatura_minima = np.min(previsoes_proximo_dia[:, 0])

    return Response(status=200, data={
        "previsao_temperatura_media": previsao_temperatura_media,
        "previsao_temperatura_maxima": previsao_temperatura_maxima,
        "previsao_temperatura_minima": previsao_temperatura_minima,
        "previsao_umidade_media": previsao_umidade_media,
        "previsao_pressao_media": previsao_pressao_media,
        "previsao_chuva_media": previsao_chuva_media,
        "previsao_vento_media": previsao_vento_media,
    })


@api_view(['GET'])
def get_historical_predict_linear_regression_ibirapuera_park(request: Request) -> Response:
    """
    Retorna uma previsão da temperatura para o Parque Ibirapuera utilizando regressão linear.

    Args:
        request (Request): Requisição HTTP.

    Returns:
        Response: Resposta HTTP contendo a previsão da temperatura, temperatura arredondada,
        umidade, pressão, velocidade do vento, direção do vento, condição climática, dica, alerta e data.
    """
    if request.method != "GET":
        return Response(status=405)

    latitude = -23.587
    longitude = -46.655

    model = import_model("modelo_regressao_linear.sav")

    predictions = get_temperature_predictions(latitude, longitude, model)

    return Response({"results": predictions}, status=200)
