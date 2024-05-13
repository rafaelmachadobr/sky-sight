import uuid

from django.contrib.gis.db import models

class HistoryForecast(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    data = models.DateField()
    hora = models.IntegerField()
    temperatura = models.FloatField()
    temperatura_maxima = models.FloatField()
    temperatura_minima = models.FloatField()
    umidade = models.FloatField()
    pressao = models.FloatField()
    velocidade_vento = models.FloatField()
    rajada_vento = models.FloatField()
    chuva = models.FloatField()