from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin, LeafletGeoAdminMixin

from .models import Image, Distrito, Concelho, Freguesia

class ConcelhoInLine(LeafletGeoAdminMixin, admin.StackedInline):
    model = Concelho
    classes = ['collapse']
    fieldsets = (
        (None, {
            'fields': ('concelho',)
        }),
        ('Map area', {
            'classes': ('collapse',),
            'fields': ('geom',),
        }),
    )

class FreguesiaInLine(LeafletGeoAdminMixin, admin.StackedInline):
    model = Freguesia
    classes = ['collapse']
    fieldsets = (
        (None, {
            'fields': ('freguesia',)
        }),
        ('Map area', {
            'classes': ('collapse',),
            'fields': ('geom',),
        }),
    )

class DistritoComplete(LeafletGeoAdmin):
    inlines = [
        ConcelhoInLine,
    ]
    search_fields = ('distrito',)

class ConcelhoComplete(LeafletGeoAdmin):
    inlines = [
        FreguesiaInLine,
    ]
    list_display = ['concelho', 'distrito']
    search_fields = ('concelho',)


class FreguesiaComplete(LeafletGeoAdmin):
    fields = ('dicofre', 'freguesia', 'concelho', 'distrito_name', 'taa', 'area_ea_ha', 'area_t_ha', 'des_simpli', 'geom')
    list_display = ['freguesia', 'concelho', 'distrito_name']
    readonly_fields = ('distrito_name',)
    search_fields = ('freguesia',)

    def distrito_name(self, obj):
        return obj.concelho.distrito
    distrito_name.short_description = 'Distrito'
    

#Admin data registration
admin.site.register(Image, LeafletGeoAdmin)
admin.site.register(Distrito, DistritoComplete)
admin.site.register(Concelho, ConcelhoComplete)
admin.site.register(Freguesia, FreguesiaComplete)