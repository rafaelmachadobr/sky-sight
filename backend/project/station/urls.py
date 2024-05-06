from django.urls import path, re_path
from . import views

app_name = 'station'

urlpatterns = [
    path('historical/predict/data/', views.get_historical_predict, name="historical_predict"),
]