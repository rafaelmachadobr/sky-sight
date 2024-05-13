from django.urls import path

from . import views

app_name = 'station'

urlpatterns = [
    path('historical/predict/data/', views.get_historical_predict, name="historical_predict"),
    path('historical/predict/linear-regression/ibirapuera-park/', views.get_historical_predict_linear_regression_ibirapuera_park,
         name="historical_predict_linear_regression"),
]
