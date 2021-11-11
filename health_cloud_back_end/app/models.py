# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator

class Keys(models.Model):
    key = models.CharField(('key'), max_length=20, blank=False)
    counter = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10), MinValueValidator(0)]
     )

    def save(self, *args, **kwargs):
        self.key = get_random_string(length=20, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVXWXYZ0123456789')
        super(Keys, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Key'
        verbose_name_plural = 'Keys'

    def __str__(self):
        return self.key

class Results(models.Model):
    key = models.ForeignKey(Keys, on_delete=models.CASCADE)
    originalImage = models.ImageField(upload_to='images')
    link = models.CharField(('link'), max_length=500, blank=False)

    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'

    def __str__(self):
        return str(self.key)