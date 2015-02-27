# -*- coding: utf-8 -*-

#from django import forms
from django.forms import ModelForm, DateInput
from estacionamientos.models import Estacionamiento, Reserva, Pago, EsquemaTarifario, EsquemaDiferenciado
from django.forms.widgets import TextInput


class EstacionamientoForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['Propietario', 'Nombre', 'Direccion', 'Telefono_1', 'Telefono_2', 'Telefono_3',
                  'Email_1', 'Email_2', 'Rif']



class EstacionamientoExtendedForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['NroPuesto', 'Apertura', 'Cierre']
#                   'Esquema_tarifario', 'HoraPicoInicio', 'HoraPicoFin', 'Tarifa', 'TarifaPico']



class EsquemaTarifarioForm(ModelForm):
    class Meta:
        model = EsquemaTarifario
        fields = ['TipoEsquema', 'Tarifa']
        
        
        
class EsquemaDiferenciadoForm(ModelForm):
    class Meta:
        model = EsquemaDiferenciado
        fields = ['HoraPicoInicio', 'HoraPicoFin', 'TarifaPico']
        


class EstacionamientoReserva(ModelForm):
    class Meta:
        model = Reserva
        fields = ['FechaInicio', 'HoraInicio', 'FechaFinal', 'HoraFinal']
        widgets = {
            'FechaInicio': DateInput(attrs={'class':'datepicker form-control',
                                          'placeholder': 'Fecha inicial de reserva'}),
            'FechaFinal': DateInput(attrs={'class':'datepicker form-control',
                                          'placeholder': 'Fecha final de reserva'}),
            'HoraInicio': TextInput(attrs={'class':'form-control',
                                          'placeholder': 'Hora inicial de reserva'}),
            'HoraFinal': TextInput(attrs={'class':'form-control',
                                          'placeholder': 'Hora final de reserva'}),
        }

        

class PagarReservaForm(ModelForm):
    class Meta:
        model = Pago
        fields = ['NroTarjeta', 'ProveedorCred', 'CedulaTitular', 'NombreTitular']


