# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Results(models.Model):
    link = models.CharField(('link'), max_length=500, blank=False)

    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'

    def __str__(self):
        return self.name