import os
from django.contrib.gis.utils import LayerMapping
from .models import Distrito, Concelho, Freguesia

# Auto-generated `LayerMapping` dictionary for Freguesia model
freguesia_mapping = {
    'dicofre': 'Dicofre',
    'freguesia': 'Freguesia',
    'concelho': {'concelho': 'Concelho'},
    'taa': 'TAA',
    'area_ea_ha': 'AREA_EA_Ha',
    'area_t_ha': 'AREA_T_Ha',
    'des_simpli': 'Des_Simpli',
    'geom': 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for Concelho model
concelho_mapping = {
    'concelho': 'Concelho',
    'distrito': {'distrito': 'Distrito'},
    'taa': 'TAA',
    'area_ea_ha': 'AREA_EA_Ha',
    'area_t_ha': 'AREA_T_Ha',
    'geom': 'MULTIPOLYGON',
}

# Auto-generated `LayerMapping` dictionary for Distritos model
distrito_mapping = {
    'distrito': 'Distrito',
    'taa': 'TAA',
    'area_ea_ha': 'AREA_EA_Ha',
    'area_t_ha': 'AREA_T_Ha',
    'geom': 'MULTIPOLYGON',
}

district_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Distritos/Distritos_WGS84.shp'),
)

concelho_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Concelhos/Concelhos_WGS84.shp'),
)

freguesia_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'Freguesias/Freguesias_WGS84.shp'),
)

def run(verbose=True):
    #Districts migration
    districts = LayerMapping(Distrito, district_shp, distrito_mapping, transform=False)
    districts.save(strict=True, verbose=verbose)

    #Concelhos migration
    concelhos = LayerMapping(Concelho, concelho_shp, concelho_mapping, transform=False)
    concelhos.save(strict=True, verbose=verbose)

    #Freguesia migration
    freguesias = LayerMapping(Freguesia, freguesia_shp, freguesia_mapping, transform=False)
    freguesias.save(strict=True, verbose=verbose)