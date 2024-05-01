import uuid

from django.contrib.gis.db import models

class HistoryForecast(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    data = models.DateField()
    temperatura = models.FloatField()
    umidade = models.FloatField()
    pressao = models.FloatField()
    velocidade_vento = models.FloatField()
    rajada_vento = models.FloatField()
    chuva = models.FloatField()