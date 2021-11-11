# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Results

# Register your models here.

class ResultsAdmin(admin.ModelAdmin):
    fields = ['id', 'link']
    readonly_fields = ['id']

admin.site.register(Results, ResultsAdmin)