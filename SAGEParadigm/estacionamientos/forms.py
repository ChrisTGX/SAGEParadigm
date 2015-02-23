# -*- coding: utf-8 -*-

#from django import forms
from django.forms import ModelForm
#from django.core.validators import RegexValidator
from estacionamientos.models import Estacionamiento, Reserva, Pago


class EstacionamientoForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['Propietario', 'Nombre', 'Direccion', 'Telefono_1', 'Telefono_2', 'Telefono_3',
                  'Email_1', 'Email_2', 'Rif']



class EstacionamientoExtendedForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['NroPuesto', 'Apertura', 'Cierre', 'Reservas_Inicio', 'Reservas_Cierre',
                  'Esquema_tarifario', 'HoraPicoInicio', 'HoraPicoFin', 'Tarifa', 'TarifaPico']



class EstacionamientoReserva(ModelForm):
    class Meta:
        model = Reserva
        fields = ['InicioReserva', 'FinalReserva']
        
# class EstacionamientoReserva(forms.Form):
#     inicio = forms.TimeField(label = 'Horario Inicio Reserva')
#     final = forms.TimeField(label = 'Horario Final Reserva')



class PagarReservaForm(ModelForm):
    class Meta:
        model = Pago
        fields = ['NroTarjeta', 'ProveedorCred']

# Este form debe ser incluido como model tambien
# class PagarReservaForm(forms.Form):
#     nro_tarjeta_credito = forms.CharField(
#                             required = True,
#                             label = "Nro. de Tarjeta",
#                             validators = [RegexValidator(
#                                                 regex = '^\d{16}$',
#                                                 message = 'Introduzca un número de tarjeta de crédito con un formato válido.'
#                                                 )])
#     proveedor_credito = forms.ChoiceField(required = True,
#                                           choices=[("Vista", "Vista"), 
#                                                    ("Mister", "Mister"), 
#                                                    ("Xpres", "Xpres")])

