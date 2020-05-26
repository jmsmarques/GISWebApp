from django.contrib.gis.db import models
from django.contrib.auth.models import User

class District(models.Model):
    district_name = models.CharField(max_length=254, primary_key=True)
    taa = models.CharField(max_length=254) #type of administrative area identificator
    area_ea_ha = models.FloatField() #total value of administrative area
    area_t_ha = models.FloatField() #total value of the district area
    geom = models.MultiPolygonField(srid=4326) #geometry representative of the boundaries of the district

    def __str__(self):
        return str.title(self.district_name)

class Municipality(models.Model):
    municipality_name = models.CharField(max_length=254, primary_key=True)
    district_name = models.ForeignKey('District', on_delete=models.CASCADE, to_field='district_name', related_name='municipality')
    taa = models.CharField(max_length=254) #type of administrative area identificator
    area_ea_ha = models.FloatField() #total value of administrative area
    area_t_ha = models.FloatField() #total value of the municipality area
    geom = models.MultiPolygonField(srid=4326) #geometry representative of the boundaries of the municipality

    def __str__(self):
        return str.title(self.municipality_name)

class Parish(models.Model):
    dicofre = models.CharField(max_length=254, primary_key=True) #Parish unique identificator
    parish_name = models.CharField(max_length=254)
    municipality_name = models.ForeignKey('Municipality', on_delete=models.CASCADE, to_field='municipality_name', related_name='parish')
    taa = models.CharField(max_length=254) #type of administrative area identificator
    area_ea_ha = models.FloatField() #total value of administrative area
    area_t_ha = models.FloatField() #total value of the parish area
    des_simpli = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=4326) #geometry representative of the boundaries of the parish

    def __str__(self):
        return self.parish_name

class ImagePoint(models.Model):
    description = models.CharField(max_length=100) #description of the image
    image = models.ImageField(upload_to='images/') #image file
    parish_name = models.ForeignKey('Parish', on_delete=models.CASCADE, default=None, related_name='images_point') #parish name where the image is located (this should be attributed automatically when adding an image)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='images_point') #image submiter username
    location = models.PointField() #image location

    def __str__(self):
        return self.description
