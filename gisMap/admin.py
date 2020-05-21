from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin, LeafletGeoAdminMixin

from .models import ImagePoint, District, Municipality, Parish

class MunicipalityInLine(LeafletGeoAdminMixin, admin.StackedInline):
    model = Municipality
    classes = ['collapse']
    fieldsets = (
        (None, {
            'fields': ('municipality_name',)
        }),
        ('Map area', {
            'classes': ('collapse',),
            'fields': ('geom',),
        }),
    )

class ParishInLine(LeafletGeoAdminMixin, admin.StackedInline):
    model = Parish
    classes = ['collapse']
    fieldsets = (
        (None, {
            'fields': ('parish_name',)
        }),
        ('Map area', {
            'classes': ('collapse',),
            'fields': ('geom',),
        }),
    )

class DistrictComplete(LeafletGeoAdmin):
    inlines = [
        MunicipalityInLine,
    ]
    search_fields = ('district_name',)

class MunicipalityComplete(LeafletGeoAdmin):
    inlines = [
        ParishInLine,
    ]
    list_display = ['municipality_name', 'district_name']
    search_fields = ('municipality_name',)


class ParishComplete(LeafletGeoAdmin):
    fields = ('dicofre', 'parish_name', 'municipality_name', 'district_name', 'taa', 'area_ea_ha', 'area_t_ha', 'des_simpli', 'geom')
    list_display = ['parish_name', 'municipality_name', 'district_name']
    readonly_fields = ('district_name',)
    search_fields = ('parish_name',)

    def district_name(self, obj):
        return obj.municipality_name.district_name
    district_name.short_description = 'District'
    

#Admin data registration
admin.site.register(ImagePoint, LeafletGeoAdmin)
admin.site.register(District, DistrictComplete)
admin.site.register(Municipality, MunicipalityComplete)
admin.site.register(Parish, ParishComplete)