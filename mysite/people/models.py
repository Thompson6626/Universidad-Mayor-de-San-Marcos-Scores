from django.db import models

class Person(models.Model):
    codigo = models.IntegerField()  
    apellidos_y_nombres = models.CharField(max_length=255,blank=False)  
    carrera_primera_opcion =  models.CharField(max_length=255, blank=False, null=False)
    puntaje = models.FloatField()  
    merito = models.CharField(max_length=255, blank=True, null=True) 
    observacion = models.CharField(max_length=255, blank=True, null=True)  
    carrera_segunda_opcion = models.CharField(max_length=255, blank=True, null=True)
    source_url = models.URLField(default = 'unkown',null=False) 

    def __str__(self):
        return f"{self.apellidos_y_nombres} ({self.codigo})"
