from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin, LeafletGeoAdminMixin

from .models import Image, Distrito, Concelho, Freguesia

class ConcelhoInLine(LeafletGeoAdminMixin, admin.StackedInline):
    model = Concelho   

class FreguesiaInLine(LeafletGeoAdminMixin, admin.StackedInline):
    model = Freguesia

class DistritoComplete(LeafletGeoAdmin):
    inline = [
        ConcelhoInLine,
    ]

class ConcelhoComplete(LeafletGeoAdmin):
    inline = [
        FreguesiaInLine
    ]

class FreguesiaComplete(LeafletGeoAdmin):
    pass

#Admin data registration
admin.site.register(Image, LeafletGeoAdmin)
admin.site.register(Distrito, DistritoComplete)
admin.site.register(Concelho, ConcelhoComplete)
admin.site.register(Freguesia, FreguesiaComplete)