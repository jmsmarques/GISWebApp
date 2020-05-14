from django.contrib.gis.db import models

class Distrito(models.Model):
    dicofre = models.CharField(max_length=254)
    distrito = models.CharField(max_length=254, primary_key=True)
    taa = models.CharField(max_length=254)
    area_ea_ha = models.FloatField()
    area_t_ha = models.FloatField()
    des_simpli = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=3763)

    def __str__(self):
        return self.distrito

class Concelho(models.Model):
    dicofre = models.CharField(max_length=254)
    concelho = models.CharField(max_length=254, primary_key=True)
    distrito = models.ForeignKey('Distrito', on_delete=models.CASCADE, to_field='distrito')
    taa = models.CharField(max_length=254)
    area_ea_ha = models.FloatField()
    area_t_ha = models.FloatField()
    des_simpli = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=3763)

    def __str__(self):
        return self.concelho


class Freguesia(models.Model):
    dicofre = models.CharField(max_length=254)
    freguesia = models.CharField(max_length=254, primary_key=True)
    concelho = models.ForeignKey('Concelho', on_delete=models.CASCADE, to_field='concelho')
    taa = models.CharField(max_length=254)
    area_ea_ha = models.FloatField()
    area_t_ha = models.FloatField()
    des_simpli = models.CharField(max_length=254)
    geom = models.MultiPolygonField(srid=3763)

    def __str__(self):
        return self.freguesia

class Image(models.Model):
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    location = models.PointField()
    freguesia = models.ForeignKey('Freguesia', on_delete=models.CASCADE)

    def __str__(self):
        return self.description
