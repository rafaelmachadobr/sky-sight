from rest_framework.decorators import api_view, parser_classes
from . import models
from rest_framework.response import Response
from
from django.http import Http404, HttpResponse
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor

@api_view(['GET'])
def get_historical_predict(request):

    history_forecast_data = models.HistoryForecast.objects.all()
    
    # Extrair características e rótulos
    X = [[data.temperatura, data.umidade, data.pressao, data.chuva] for data in history_forecast_data]
    y = [d.temperatura for d in history_forecast_data]  #Variavel alvo

    # Inicializar e treinar o modelo Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X, y)

    dados_hoje = models.HistoryForecast.objects.filter(data=datetime.date.today())
    dados_hoje = dados_hoje.first()

    dados_previsao = [[dados_hoje.temperatura, dados_hoje.umidade, dados_hoje.pressao, dados_hoje.chuva]]
    previsao = rf_model.predict(dados_previsao)
    print("Previsão para o dia seguinte:", previsao)

    return Response(satus=200)