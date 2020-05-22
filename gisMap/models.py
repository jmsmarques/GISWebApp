from django.contrib.gis.db import models
from django.contrib.auth.models import User

class District(models.Model):
    district_name = models.CharField(max_length=254, primary_key=True)
    taa = models.CharField(max_length=254)
    area_ea_ha = models.FloatField()
    area_t_ha = models.FloatField()
    geom = models.MultiPolygonField()

    def __str__(self):
        return str.title(self.district_name)

class Municipality(models.Model):
    municipality_name = models.CharField(max_length=254, primary_key=True)
    district_name = models.ForeignKey('District', on_delete=models.CASCADE, to_field='district_name', related_name='municipality')
    taa = models.CharField(max_length=254)
    area_ea_ha = models.FloatField()
    area_t_ha = models.FloatField()
    geom = models.MultiPolygonField()

    def __str__(self):
        return str.title(self.municipality_name)


class Parish(models.Model):
    dicofre = models.CharField(max_length=254, primary_key=True)
    parish_name = models.CharField(max_length=254)
    municipality_name = models.ForeignKey('Municipality', on_delete=models.CASCADE, to_field='municipality_name', related_name='parish')
    taa = models.CharField(max_length=254)
    area_ea_ha = models.FloatField()
    area_t_ha = models.FloatField()
    des_simpli = models.CharField(max_length=254)
    geom = models.MultiPolygonField()

    def __str__(self):
        return self.parish_name
    
class ImagePoint(models.Model):
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    parish_name = models.ForeignKey('Parish', on_delete=models.CASCADE, default=None, related_name='images_point')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='images_point')
    location = models.PointField()

    def __str__(self):
        return self.description
