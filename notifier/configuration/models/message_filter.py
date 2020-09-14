from django.db import models


class MessageFilter(models.Model):
    name = models.CharField(max_length=100)
