# -*- coding: utf-8 -*-

from django.core.validators import RegexValidator
from django.db import models
from django.forms import ModelForm


class Estacionamiento(models.Model):
	# propietario=models.ForeignKey(Propietario)
	Propietario = models.CharField(max_length = 50, help_text = "Nombre Propio")
	Nombre = models.CharField(max_length = 50)
	Direccion = models.TextField(max_length = 120)

	Telefono_1 = models.CharField(blank = True, null = True, max_length = 30)
	Telefono_2 = models.CharField(blank = True, null = True, max_length = 30)
	Telefono_3 = models.CharField(blank = True, null = True, max_length = 30)

	Email_1 = models.EmailField(blank = True, null = True)
	Email_2 = models.EmailField(blank = True, null = True)

	Rif = models.CharField(max_length = 12)

	Esquema_tarifario = models.CharField(max_length = 4, blank = True, null = True)
	Tarifa = models.DecimalField(max_length = 50, max_digits=6, decimal_places=2, blank = True, null = True)
	Apertura = models.TimeField(blank = True, null = True)
	Cierre = models.TimeField(blank = True, null = True)
	Reservas_Inicio = models.TimeField(blank = True, null = True)
	Reservas_Cierre = models.TimeField(blank = True, null = True)
	NroPuesto = models.IntegerField(blank = True, null = True)


# class ExtendedModel(models.Model):
# 	Estacionamiento = models.ForeignKey(Estacionamiento, primary_key = True)

# class EstacionamientoModelForm(EstacionamientoForm):
# 	class Meta:
# 		model = EstacionamientoModel
# 		fields = ['propietario', 'nombre', 'direccion', 'telefono_1', 'telefono_2', 'telefono_3', 'email_1',
# 				'email_2', 'rif', 'tarifa', 'horarioin', 'horariout', 'horario_resein', 'horario_reserout']

# class Propietario(models.Model):
	# nombre = models.CharField(max_length = 50, help_text = "Nombre Propio")

# class EstadoEstacionamiento(models.Model):
	#

# class PuestosModel(models.Model):
# 	estacionamiento = models.ForeignKey(ExtendedModel)


class ReservasModel(models.Model):
	Estacionamiento = models.ForeignKey(Estacionamiento)
	Puesto = models.IntegerField()
	InicioReserva = models.TimeField()
	FinalReserva = models.TimeField()
	Pagada = models.BooleanField(blank = True, null = True)

