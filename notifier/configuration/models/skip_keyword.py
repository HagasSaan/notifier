from django.db import models


class SkipKeyword(models.Model):
    word = models.CharField(max_length=30)

    def __str__(self):
        return self.word
