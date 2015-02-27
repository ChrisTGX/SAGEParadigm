# -*- coding: utf-8 -*-

#from django import forms
from django.forms import ModelForm, DateInput
from estacionamientos.models import Estacionamiento, Reserva, Pago, EsquemaTarifario, EsquemaDiferenciado,\
    PROVCRED_Choices, SCHEME_Choices
from django.forms.widgets import TextInput, Select
from logging import PlaceHolder


class EstacionamientoForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['Propietario', 'Nombre', 'Direccion', 'Telefono_1', 'Telefono_2', 'Telefono_3',
                  'Email_1', 'Email_2', 'Rif']
        widgets = {
            'Propietario': TextInput(attrs={'class':'form-control',
                                            'placeholder': 'Ej: Pedro Pérez'}),
            'Nombre': TextInput(attrs={'class':'form-control',
                                       'placeholder': 'Ej: Mi Estacionamiento'}),
            'Direccion': TextInput(attrs={'class':'form-control',
                                          'placeholder': 'Ej: Av. Libertador, etc'}),
            'Telefono_1': TextInput(attrs={'class':'form-control',
                                           'placeholder': 'Ej: 0424-1112233'}),
            'Telefono_2': TextInput(attrs={'class':'form-control',
                                           'placeholder': 'Ej: 02121234567'}),
            'Telefono_3': TextInput(attrs={'class':'form-control',
                                           'placeholder': 'Ej: 0412-1234567'}),
            'Email_1': TextInput(attrs={'class':'form-control',
                                        'placeholder': 'Ej: mi_email@mi_dominio.com'}),
            'Email_2': TextInput(attrs={'class':'form-control',
                                        'placeholder': 'Ej: mi_email@mi_dominio.com'}),
            'Rif': TextInput(attrs={'class':'form-control',
                                    'placeholder': 'Ej: V-123456789'}),
        }



class EstacionamientoExtendedForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['NroPuesto', 'Apertura', 'Cierre']
        widgets = {
                   'NroPuesto': TextInput(attrs={'class':'form-control',
                                                 'placeholder':'Ej: 10'}),
                   'Apertura': TextInput(attrs={'class':'form-control',
                                                'placeholder':'Ej: 5:00'}),
                   'Cierre': TextInput(attrs={'class':'form-control',
                                              'placeholder':'Ej: 18:00'}),
                   }



class EsquemaTarifarioForm(ModelForm):
    class Meta:
        model = EsquemaTarifario
        fields = ['TipoEsquema', 'Tarifa']
        widgets = {
            'TipoEsquema': Select(choices=SCHEME_Choices, 
                                    attrs={'class':'form-control'}),
            'Tarifa': TextInput(attrs={'class':'form-control',
                                       'placeholder': 'Ej: 100'}),
        }
        
        
        
class EsquemaDiferenciadoForm(ModelForm):
    class Meta:
        model = EsquemaDiferenciado
        fields = ['HoraPicoInicio', 'HoraPicoFin', 'TarifaPico']
        widgets = {
                   'HoraPicoInicio': TextInput(attrs={'class':'form-control',
                                                      'placeholder': 'Ej: 15:00'}),
                   'HoraPicoFin': TextInput(attrs={'class':'form-control',
                                                   'placeholder': 'Ej: 18:00'}),
                   'TarifaPico': TextInput(attrs={'class':'form-control',
                                                  'placeholder': 'Ej: 100'}),
                  }
        


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
        widgets = {
            'ProveedorCred': Select(choices=PROVCRED_Choices, 
                                    attrs={'class':'form-control'}),
            'NroTarjeta': DateInput(attrs={'class':'form-control',
                                           'placeholder': 'Ej: 1111-2222-3333-4444'}),
            'CedulaTitular': TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Ej: V-12345678'}),
            'NombreTitular': TextInput(attrs={'class':'form-control',
                                              'placeholder': 'Ej: Pedro Pérez'}),
        }


