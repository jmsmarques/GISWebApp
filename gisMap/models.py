from django.contrib.gis.db import models

class Distrito(models.Model):
    distrito = models.CharField(max_length=254, primary_key=True)
    taa = models.CharField(max_length=254)
    area_ea_ha = models.FloatField()
    area_t_ha = models.FloatField()
    geom = models.MultiPolygonField()

    def __str__(self):
        return str.title(self.distrito)

class Concelho(models.Model):
    concelho = models.CharField(max_length=254, primary_key=True)
    distrito = models.ForeignKey('Distrito', on_delete=models.CASCADE, to_field='distrito', related_name='concelho')
    taa = models.CharField(max_length=254)
    area_ea_ha = models.FloatField()
    area_t_ha = models.FloatField()
    geom = models.MultiPolygonField()

    def __str__(self):
        return str.title(self.concelho)


class Freguesia(models.Model):
    dicofre = models.CharField(max_length=254, primary_key=True)
    freguesia = models.CharField(max_length=254)
    concelho = models.ForeignKey('Concelho', on_delete=models.CASCADE, to_field='concelho', related_name='freguesia')
    taa = models.CharField(max_length=254)
    area_ea_ha = models.FloatField()
    area_t_ha = models.FloatField()
    des_simpli = models.CharField(max_length=254)
    geom = models.MultiPolygonField()

    def __str__(self):
        return self.freguesia

class Image(models.Model):
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    freguesia = models.ForeignKey('Freguesia', on_delete=models.CASCADE, default=None)
    location = models.PointField()

    def __str__(self):
        return self.description
