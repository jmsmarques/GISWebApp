from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Image, Distrito, Concelho, Freguesia

# admin.site.register(District, LeafletGeoAdmin)
admin.site.register(Image, LeafletGeoAdmin)
admin.site.register(Distrito, LeafletGeoAdmin)
admin.site.register(Concelho, LeafletGeoAdmin)
admin.site.register(Freguesia, LeafletGeoAdmin)

