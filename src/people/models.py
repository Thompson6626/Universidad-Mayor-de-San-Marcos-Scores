from django.db import models

class Person(models.Model):
    codigo = models.CharField(max_length=255)
    apellidos_y_nombres = models.CharField(max_length=255)
    carrera_primera_opcion = models.CharField(max_length=255)
    puntaje = models.FloatField(null=True, blank=True)
    merito = models.CharField(max_length=255, null=True, blank=True) 
    observacion = models.CharField(max_length=255, null=True, blank=True)
    carrera_segunda_opcion = models.CharField(max_length=255, null=True, blank=True)
    fecha = models.CharField(max_length=255, null=True, blank=True)
    modalidad_de_ingreso = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f"{self.apellidos_y_nombres} ({self.codigo})"