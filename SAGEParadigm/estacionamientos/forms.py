# -*- coding: utf-8 -*-

#from django import forms
from django.forms import ModelForm
from django import forms
from estacionamientos.models import Estacionamiento, Reserva, Pago, EsquemaTarifario, EsquemaDiferenciado
from cProfile import label


class EstacionamientoForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['Propietario', 'Nombre', 'Direccion', 'Telefono_1', 'Telefono_2', 'Telefono_3',
                  'Email_1', 'Email_2', 'Rif']



class EstacionamientoExtendedForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['NroPuesto', 'Apertura', 'Cierre', 'Reservas_Inicio', 'Reservas_Cierre']



class EsquemaTarifarioForm(ModelForm):
    class Meta:
        model = EsquemaTarifario
        fields = ['TipoEsquema', 'Tarifa']
        
        
        
class EsquemaDiferenciadoForm(ModelForm):
    class Meta:
        model = EsquemaDiferenciado
        fields = ['HoraPicoInicio', 'HoraPicoFin', 'TarifaPico']
        


class EstacionamientoReserva(forms.Form):
    FechaInicio = forms.DateField(required=True, input_formats=['%d/%m/%Y'], label="Fecha de Inicio")
    HoraInicio = forms.TimeField(required=True, label="Hora de Inicio")
    FechaFinal = forms.DateField(required=True, input_formats=['%d/%m/%Y'], label="Fecha de Fin")
    HoraFinal = forms.TimeField(required=True, label="Hora de Fin")
#     class Meta:
#         model = Reserva
#         fields = ['FechaInicio', 'HoraInicio', 'FechaFinal', 'HoraFinal']

        

class PagarReservaForm(ModelForm):
    class Meta:
        model = Pago
        fields = ['NroTarjeta', 'ProveedorCred', 'CedulaTitular', 'NombreTitular']


