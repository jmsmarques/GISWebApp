from django.contrib.gis.db import models
from django.contrib.auth.models import User

class District(models.Model):
    di = models.CharField(max_length=254, primary_key=True) #district unique identifier
    district_name = models.CharField(max_length=254, unique=True) #district name
    area_ea_ha = models.FloatField() #total value of administrative area
    area_t_ha = models.FloatField() #total value of the district area
    geom = models.MultiPolygonField(srid=4326) #geometry representative of the boundaries of the district

    def __str__(self):
        return str.title(self.district_name)


class Municipality(models.Model):
    dico = models.CharField(max_length=254, primary_key=True) #Municipality unique identifier
    municipality_name = models.CharField(max_length=254, unique=True) #name of the municipality
    district_name = models.ForeignKey('District', on_delete=models.CASCADE, to_field='di', related_name='municipality') #district name where this municipality belongs
    area_ea_ha = models.FloatField() #total value of administrative area
    area_t_ha = models.FloatField() #total value of the municipality area
    geom = models.MultiPolygonField(srid=4326) #geometry representative of the boundaries of the municipality

    def __str__(self):
        return str.title(self.municipality_name)

class Parish(models.Model):
    dicofre = models.CharField(max_length=254, primary_key=True) #Parish unique identifier
    parish_name = models.CharField(max_length=254) #name of the parish
    municipality_name = models.ForeignKey('Municipality', on_delete=models.CASCADE, to_field='dico', related_name='parish') #municipality name where this district belongs
    area_ea_ha = models.FloatField() #total value of administrative area
    area_t_ha = models.FloatField() #total value of the parish area
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
