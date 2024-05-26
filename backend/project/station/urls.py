from django.urls import path

from . import views

app_name = 'station'

urlpatterns = [
    path('historical/predict/random-forest/one-day/ibirapuera-park/', views.get_historical_predict_random_forest, name="historical_predict"),
    path('historical/predict/linear-regression/ibirapuera-park/', views.get_historical_predict_linear_regression_ibirapuera_park,
         name="historical_predict_linear_regression"),
]