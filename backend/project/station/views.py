import numpy as np

from warnings import filterwarnings


from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .utils import get_temperature_predictions, import_model, remove_nan_samples

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

from . import models
# filterwarnings('ignore')

@api_view(['GET'])
def get_historical_predict(request):
    # Filtrar todos os dados disponíveis para a data especificada
    data_day = models.HistoryForecast.objects.filter(data="2024-05-11")

    if not data_day.exists():
        return Response(status=404, data={"message": "Não há dados disponíveis para o dia especificado."})

    # Extrair características e rótulos de todos os dados do dia
    X = [[data.temperatura_maxima, data.temperatura_minima, data.umidade, data.pressao, data.chuva] for data in data_day]
    y = [[data.temperatura, data.umidade, data.pressao, data.chuva] for data in data_day]  # Variáveis alvo

    # Verificar e tratar valores ausentes nas variáveis de entrada
    X, y = remove_nan_samples(X, y)

    if len(X) == 0:
        return Response(status=400, data={"message": "Todos os dados estão ausentes."})

    # Normalizar as características, se necessário
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Inicializar e treinar o modelo Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

    # Preparar os dados de previsão para o próximo dia
    data_predict_next_day = [[data.temperatura_maxima, data.temperatura_minima, data.umidade, data.pressao, data.chuva] for data in data_day]
    data_predict_next_day = scaler.transform(data_predict_next_day)

    # Fazer a previsão para todos os dados do próximo dia
    predict_next_day = rf_model.predict(data_predict_next_day)

    # Calcular a média das previsões para o próximo dia
    predict_medium = np.mean(predict_next_day, axis=0)
    print("Previsão média para o próximo dia:", predict_medium)

    previsao_temperatura_media = predict_medium[0]
    previsao_umidade_media = predict_medium[1]
    previsao_pressao_media = predict_medium[2]
    previsao_chuva_media = predict_medium[3]

    previsao_temperatura_maxima = np.max(predict_next_day[:, 0])
    previsao_temperatura_minima = np.min(predict_next_day[:, 0])

    data = {
        "previsao_temperatura_media": previsao_temperatura_media,
        "previsao_temperatura_maxima": previsao_temperatura_maxima,
        "previsao_temperatura_minima": previsao_temperatura_minima,
        "previsao_umidade_media": previsao_umidade_media,
        "previsao_pressao_media": previsao_pressao_media,
        "previsao_chuva_media": previsao_chuva_media
    }

    return Response(data, status=200)


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
