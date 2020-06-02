import os
from django.contrib.gis.utils import LayerMapping
from .models import District, Municipality, Parish

# Auto-generated `LayerMapping` dictionary for Portugal_Districts model
districts_mapping = {
    'di': 'Di',
    'district_name': 'District',
    'area_ea_ha': 'AREA_EA_Ha',
    'area_t_ha': 'AREA_T_Ha',
    'geom': 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for Portugal_Municipalities model
municipalities_mapping = {
    'dico': 'Dico',
    'municipality_name': 'Municipali',
    'district_name': {'di': 'Di'},
    'area_ea_ha': 'AREA_EA_Ha',
    'area_t_ha': 'AREA_T_Ha',
    'geom': 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for Portugal_Parishes model
parishes_mapping = {
    'dicofre': 'Dicofre',
    'parish_name': 'Parish',
    'municipality_name': {'dico': 'Dico'},
    'area_ea_ha': 'AREA_EA_Ha',
    'area_t_ha': 'AREA_T_Ha',
    'geom': 'MULTIPOLYGON',
}


district_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Districts/Portugal_Districts.shp'),
)

municipality_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Municipalities/Portugal_Municipalities.shp'),
)

parish_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Parishes/Portugal_Parishes.shp'),
)

def run(verbose=True):
    #Districts migration
    districts = LayerMapping(District, district_shp, districts_mapping, transform=False)
    districts.save(strict=True, verbose=verbose)

    #Municipalities migration
    municipalities = LayerMapping(Municipality, municipality_shp, municipalities_mapping, transform=False)
    municipalities.save(strict=True, verbose=verbose)

    #Parishies migration
    parishies = LayerMapping(Parish, parish_shp, parishes_mapping, transform=False)
    parishies.save(strict=True, verbose=verbose)
