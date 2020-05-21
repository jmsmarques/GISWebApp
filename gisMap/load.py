import os
from django.contrib.gis.utils import LayerMapping
from .models import District, Municipality, Parish

# Auto-generated `LayerMapping` dictionary for Freguesia model
parish_mapping = {
    'dicofre': 'Dicofre',
    'parish_name': 'Freguesia',
    'municipality_name': {'municipality_name': 'Concelho'},
    'taa': 'TAA',
    'area_ea_ha': 'AREA_EA_Ha',
    'area_t_ha': 'AREA_T_Ha',
    'des_simpli': 'Des_Simpli',
    'geom': 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for Concelho model
municipality_mapping = {
    'municipality_name': 'Concelho',
    'district_name': {'district_name': 'Distrito'},
    'taa': 'TAA',
    'area_ea_ha': 'AREA_EA_Ha',
    'area_t_ha': 'AREA_T_Ha',
    'geom': 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for Distritos model
district_mapping = {
    'district_name': 'Distrito',
    'taa': 'TAA',
    'area_ea_ha': 'AREA_EA_Ha',
    'area_t_ha': 'AREA_T_Ha',
    'geom': 'MULTIPOLYGON',
}

district_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Distritos/Distritos_WGS84.shp'),
)

municipality_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Concelhos/Concelhos_WGS84.shp'),
)

parish_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Freguesias/Freguesias_WGS84.shp'),
)

def run(verbose=True):
    #Districts migration
    districts = LayerMapping(District, district_shp, district_mapping, transform=False)
    districts.save(strict=True, verbose=verbose)

    #Municipalities migration
    municipalities = LayerMapping(Municipality, municipality_shp, municipality_mapping, transform=False)
    municipalities.save(strict=True, verbose=verbose)

    #Parishies migration
    parishies = LayerMapping(Parish, parish_shp, parish_mapping, transform=False)
    parishies.save(strict=True, verbose=verbose)