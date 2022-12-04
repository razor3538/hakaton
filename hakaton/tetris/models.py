from django.db import models


class Palete(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
