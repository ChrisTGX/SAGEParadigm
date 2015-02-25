# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator

# Validators

NAME_Validator = RegexValidator(
					regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
					message = 'Sólo debe contener letras.'
					)

RIF_Validator = RegexValidator(
				regex = '^[JVD]-?\d{8}-?\d$', 
				message = 'Introduzca un RIF con un formato válido.'
				)

IDDOC_Validator = RegexValidator(
					regex = '^[VE]-?\d{1,8}$',
					message = "Introduzca un número de cédula con formato válido."
					)

CREDITCARD_Validator = RegexValidator(
						regex = '^\d{16}$',
						message = 'Introduzca un número de tarjeta de crédito con un formato válido.'
						)

PHONE_Validator = RegexValidator(
					regex = '^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-?\d{7}',
					message = 'Debe introducir un formato válido.'					
					)

# Choices

SCHEME_Choices = [("1", "Por hora"),
					("2", "Por hora y fracción"),
					("3", "Por minuto"),
					("4", "Diferenciado por hora")]

PROVCRED_Choices = [("Vista", "Vista"),
					("Mister", "Mister"),
					("Xpres", "Xpres")]


# Models

class Estacionamiento(models.Model):
	Propietario = models.CharField(max_length = 50, help_text = "Nombre del Propietario", validators = [NAME_Validator], verbose_name="Nombre del Propietario")
	Nombre = models.CharField(max_length = 50, verbose_name="Nombre del Estacionamiento")
	Direccion = models.TextField(max_length = 120, verbose_name="Dirección")

	Telefono_1 = models.CharField(blank = True, null = True, max_length = 30, validators = [PHONE_Validator], verbose_name="Teléfono 1")
	Telefono_2 = models.CharField(blank = True, null = True, max_length = 30, validators = [PHONE_Validator], verbose_name="Teléfono 2")
	Telefono_3 = models.CharField(blank = True, null = True, max_length = 30, validators = [PHONE_Validator], verbose_name="Teléfono 3")

	Email_1 = models.EmailField(blank = True, null = True, verbose_name="Email 1")
	Email_2 = models.EmailField(blank = True, null = True, verbose_name="Email 2")

	Rif = models.CharField(max_length = 12, validators = [RIF_Validator], verbose_name="RIF")

# 	Esquema_tarifario = models.CharField(max_length = 4, choices = SCHEME_Choices, blank = True, null = True, verbose_name="Esquema Tarifario")
# 	Tarifa = models.DecimalField(max_digits=6, decimal_places=2, blank = True, null = True, verbose_name="Tarifa")
# 	HoraPicoInicio = models.TimeField(blank = True, null = True, verbose_name="Inicio de Hora Pico")
# 	HoraPicoFin = models.TimeField(blank = True, null = True, verbose_name="Fin de Hora Pico")
# 	TarifaPico = models.DecimalField(max_digits=6, decimal_places=2, blank = True, null = True, verbose_name="Tarifa de Hora Pico")
	
	Apertura = models.TimeField(blank = True, null = True, verbose_name="Horario de Apertura")
	Cierre = models.TimeField(blank = True, null = True, verbose_name="Horario de Cierre")
	Reservas_Inicio = models.TimeField(blank = True, null = True, verbose_name="Horario Inicio de Reserva")
	Reservas_Cierre = models.TimeField(blank = True, null = True, verbose_name="Horario Fin de Reserva")
	
	NroPuesto = models.IntegerField(blank = True, null = True, verbose_name="Número de Puestos")

	def __str__(self):
		return "Estacionamiento " + self.Nombre



class EsquemaTarifario(models.Model):
	Estacionamiento = models.ForeignKey(Estacionamiento, primary_key = True, unique = True, editable = False)
	TipoEsquema = models.CharField(max_length=50, choices = SCHEME_Choices, verbose_name="Tipo de Esquema", null = True)
	Tarifa = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Tarifa", null = True)
	
	def __str__(self):
		return "Esquema Tarifario tipo " + str(self.TipoEsquema) + " del estacionamiento " + str(self.Estacionamiento) + " | Tarifa: " + str(self.Tarifa)
	
	
	
class EsquemaDiferenciado(models.Model):
	EsquemaTarifario = models.ForeignKey(EsquemaTarifario, primary_key = True, unique = True, editable = False)
	HoraPicoInicio = models.DateTimeField(blank = True, null = True, verbose_name="Inicio de Hora Pico")
	HoraPicoFin = models.DateTimeField(blank = True, null = True, verbose_name="Fin de Hora Pico")
	TarifaPico = models.DecimalField(max_digits=6, decimal_places=2, blank = True, null = True, verbose_name="Tarifa de Hora Pico")

	def __str__(self):
		return "Esquema Tarifario Diferenciado " + str(self.EsquemaTarifario) + " | Tarifa Pico: " + str(self.TarifaPico) 



class Reserva(models.Model):
	Estacionamiento = models.ForeignKey(Estacionamiento)
	Puesto = models.IntegerField()
	InicioReserva = models.TimeField(verbose_name="Hora de Inicio")
	FinalReserva = models.TimeField(verbose_name="Hora de Final")
	Pagada = models.NullBooleanField(blank = True, null = True)

	def __str__(self):
		return "Reserva del puesto " + str(self.Puesto) + " en " + self.Estacionamiento.Nombre + " de " + str(self.InicioReserva) + " a " + str(self.FinalReserva)



class Pago(models.Model):
	ID_Pago = models.ForeignKey(Reserva, primary_key=True, editable=False)
	NroTarjeta = models.CharField(max_length=16, null = True, validators=[CREDITCARD_Validator], verbose_name="Número de Tarjeta")
	NombreTitular = models.CharField(max_length=50, null = True, validators=[NAME_Validator], verbose_name="Nombre del Titular")
	CedulaTitular = models.CharField(max_length=10, null = True, validators=[IDDOC_Validator], verbose_name="Cédula del Titular")
	ProveedorCred = models.CharField(max_length=10, null = True, choices=PROVCRED_Choices, verbose_name="Proveedor de Crédito")
	Monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto", null = True)
	
	def __str__(self):
		return "Pago de la " + str(self.ID_Pago)
