# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Results, Keys, HeatmapLink

# Register your models here.

class ResultsAdmin(admin.ModelAdmin):
    fields = ['id', 'key', 'originalImage', 'heatmaps_links', 'created_at']
    readonly_fields = ['id', 'originalImage', 'heatmaps_links', 'created_at']
    actions=['really_delete_selected']

    def get_actions(self, request):
        actions = super(ResultsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 result entry was"
        else:
            message_bit = "%s result entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    really_delete_selected.short_description = "Delete selected entries"

class KeysAdmin(admin.ModelAdmin):
    fields = ['id', 'key', 'counter', 'created_at']
    readonly_fields = ['id', 'key', 'counter', 'created_at']
    actions=['really_delete_selected']

    def get_actions(self, request):
        actions = super(KeysAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 key entry was"
        else:
            message_bit = "%s key entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    really_delete_selected.short_description = "Delete selected entries"

class HeatmapsLinkAdmin(admin.ModelAdmin):
    fields = ['id', 'pathology', 'link']
    readonly_fields = ['id', 'pathology', 'link']
    actions=['really_delete_selected']

    def get_actions(self, request):
        actions = super(HeatmapsLinkAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def really_delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()

        if queryset.count() == 1:
            message_bit = "1 link entry was"
        else:
            message_bit = "%s link entries were" % queryset.count()
        self.message_user(request, "%s successfully deleted." % message_bit)
    really_delete_selected.short_description = "Delete selected entries"

admin.site.register(Results, ResultsAdmin)
admin.site.register(Keys, KeysAdmin)
admin.site.register(HeatmapLink, HeatmapsLinkAdmin)