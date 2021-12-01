# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from ..settings import API_URL
import os

class Keys(models.Model):
    key = models.CharField(('key'), max_length=20, blank=False)
    counter = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = get_random_string(length=20, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVXWXYZ0123456789')
        super(Keys, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Key'
        verbose_name_plural = 'Keys'

    def __str__(self):
        return self.key

class HeatmapLink(models.Model):
    pathology = models.CharField(max_length=50, blank=False)
    link = models.CharField(max_length=100, blank=False)

    def delete(self, *args, **kwargs):
        img_path = self.link.split(API_URL)[1]
        if os.path.exists(img_path):
                os.remove(img_path)
        super(HeatmapLink, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'HeatmapLink'
        verbose_name_plural = 'HeatmapLinks'

    def __str__(self):
        return self.link

class Results(models.Model):
    key = models.ForeignKey(Keys, on_delete=models.CASCADE)
    originalImage = models.ImageField(upload_to='images')
    heatmaps_links = models.ManyToManyField(HeatmapLink)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.key.counter = self.key.counter - 1
        self.key.save()
        self.originalImage.delete(save = False)

        for heatmap_link in self.heatmaps_links.all():
            heatmap_link.delete()

        super(Results, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'

    def __str__(self):
        return str(self.key)

@receiver(pre_delete, sender=Results)
def delete_result(sender, instance, signal, *args, **kwargs):
    instance.key.counter = instance.key.counter - 1
    instance.key.save()
    instance.originalImage.delete(save = False)

    for heatmap_link in instance.heatmaps_links.all():
        heatmap_link.delete()