# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Results, Keys

# Register your models here.

class ResultsAdmin(admin.ModelAdmin):
    fields = ['id', 'key', 'originalImage', 'link']
    readonly_fields = ['id']

class KeysAdmin(admin.ModelAdmin):
    fields = ['id', 'key', 'counter']
    readonly_fields = ['id', 'key', 'counter']

admin.site.register(Results, ResultsAdmin)
admin.site.register(Keys, KeysAdmin)