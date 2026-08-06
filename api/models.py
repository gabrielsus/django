# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdministradoresConsorcio(models.Model):
    id = models.BigAutoField(primary_key=True)
    matricula = models.IntegerField(unique=True)
    nombre = models.TextField()
    fecha_inscripcion = models.DateField()
    oneroso = models.CharField(max_length=10)
    correo = models.TextField(blank=True, null=True)
    sanciones = models.TextField()
    banco_codigo = models.ForeignKey('Bancos',on_delete=models.SET_NULL, db_column='banco_codigo', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'administradores_consorcio'

    
class Bancos(models.Model):
    codigo = models.CharField(primary_key=True, max_length=3)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)

    class Meta:
        managed = True
        db_table = 'bancos'


class Comprobantes(models.Model):
    nombre_archivo = models.CharField(max_length=255, blank=True, null=True)
    path_archivo = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'comprobantes'


class Tareas(models.Model):
    titulo = models.CharField(max_length=100)
    completada = models.BooleanField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tareas'
