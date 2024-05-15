import numpy as np

from datetime import datetime
from warnings import filterwarnings


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

    # data_atual = datetime.now().date()
    data_atual = datetime.strptime("2024-05-14", "%Y-%m-%d").date()

    dados_do_dia = models.HistoryForecast.objects.filter(dt_sensing__date=data_atual)

    if not dados_do_dia.exists():
        return Response(status=404, data={"message": "Não há dados disponíveis para o dia atual."})

    # Extrair características e rótulos dos dados do dia atual
    X = [[data.temperatura_maxima, data.temperatura_minima, data.umidade, data.pressao, data.chuva, data.velocidade_vento] for data in dados_do_dia]
    y = [[data.temperatura] for data in dados_do_dia]  # Variável alvo (apenas temperatura)

    # Verificar e tratar valores ausentes nas variáveis de entrada
    X, y = remove_nan_samples(X, y)

    # Verificar se restaram amostras após remover as com valores ausentes
    if len(X) == 0:
        return Response(status=400, data={"message": "Todos os dados estão ausentes para o dia atual."})

    # Normalizar as características, se necessário
    scaler = StandardScaler()
    X_normalized = scaler.fit_transform(X)

    # Inicializar e treinar o modelo Random Forest com os dados do dia atual
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_normalized, y)

    dados_previsao_proximo_dia = X_normalized

    # Faz a previsão para todos os dados do próximo dia
    previsoes_proximo_dia = rf_model.predict(dados_previsao_proximo_dia)
    previsao_media_proximo_dia = np.mean(previsoes_proximo_dia)

    # Estimar a temperatura máxima como a média mais o desvio padrão
    desvio_padrao = np.std(previsoes_proximo_dia)
    previsao_temperatura_maxima = previsao_media_proximo_dia + desvio_padrao

    # Previsão para temperatura mínima (aproximação simples)
    previsao_temperatura_minima = previsao_media_proximo_dia - 5

    previsao_umidade_media = np.mean(X[:, 2] * scaler.scale_[2] + scaler.mean_[2])
    previsao_chuva_media = np.mean(X[:, 4] * scaler.scale_[4] + scaler.mean_[4])
    previsao_pressao_media = np.mean(X[:, 3] * scaler.scale_[3] + scaler.mean_[3])
    previsao_vento_media = np.mean(X[:, 5] * scaler.scale_[5] + scaler.mean_[5])

    return Response(status=200, data={
        "previsao_temperatura_media": previsao_media_proximo_dia,
        "previsao_temperatura_maxima": previsao_temperatura_maxima,
        "previsao_temperatura_minima": previsao_temperatura_minima,
        "previsao_umidade_media": previsao_umidade_media,
        "previsao_chuva_media": previsao_chuva_media,
        "previsao_pressao_media": previsao_pressao_media,
        "previsao_vento_media": previsao_vento_media
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
