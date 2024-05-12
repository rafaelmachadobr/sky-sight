from warnings import filterwarnings

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .utils import importar_modelo, obter_previsoes_temperatura

# from . import models
filterwarnings('ignore')

# @api_view(['GET'])
# def get_historical_predict(request):

#     history_forecast_data = models.HistoryForecast.objects.all()

#     # Extrair características e rótulos
#     X = [[data.temperatura, data.umidade, data.pressao, data.chuva] for data in history_forecast_data]
#     y = [d.temperatura for d in history_forecast_data]  #Variavel alvo

#     # Inicializar e treinar o modelo Random Forest
#     rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
#     rf_model.fit(X, y)

#     dados_hoje = models.HistoryForecast.objects.filter(data=datetime.date.today())
#     dados_hoje = dados_hoje.first()

#     dados_previsao = [[dados_hoje.temperatura, dados_hoje.umidade, dados_hoje.pressao, dados_hoje.chuva]]
#     previsao = rf_model.predict(dados_previsao)
#     print("Previsão para o dia seguinte:", previsao)

#     return Response(satus=200)


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

    modelo = importar_modelo("modelo_regressao_linear.sav")

    previsoes = obter_previsoes_temperatura(latitude, longitude, modelo)

    return Response({"results": previsoes}, status=200)
