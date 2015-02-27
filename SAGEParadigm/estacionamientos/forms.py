# -*- coding: utf-8 -*-

#from django import forms
from django.forms import ModelForm, DateInput, BooleanField
from estacionamientos.models import Estacionamiento, Reserva, Pago, EsquemaTarifario, EsquemaDiferenciado,\
    PROVCRED_Choices, SCHEME_Choices
from django.forms.widgets import TextInput, Select, CheckboxInput


class EstacionamientoForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['Propietario', 'Nombre', 'Direccion', 'Telefono_1', 'Telefono_2', 'Telefono_3',
                  'Email_1', 'Email_2', 'Rif']
        widgets = {
            'Propietario': TextInput(attrs={'class':'form-control fields_margin',
                                            'placeholder': 'Propietario (Ej: Pedro Pérez)'}),
            'Nombre': TextInput(attrs={'class':'form-control fields_margin',
                                       'placeholder': 'Nombre Estacionamiento (Ej: Bull)'}),
            'Direccion': TextInput(attrs={'class':'form-control fields_margin',
                                          'placeholder': 'Dirección (Ej: Av. Libertador, ...)'}),
            'Telefono_1': TextInput(attrs={'class':'form-control fields_margin',
                                           'placeholder': 'Teléfono 1 (Ej: 0424-1112233)'}),
            'Telefono_2': TextInput(attrs={'class':'form-control fields_margin',
                                           'placeholder': 'Teléfono 2 (Ej: 02121234567)'}),
            'Telefono_3': TextInput(attrs={'class':'form-control fields_margin',
                                           'placeholder': 'Teléfono 3 (Ej: 0412-1234567)'}),
            'Email_1': TextInput(attrs={'class':'form-control fields_margin',
                                        'placeholder': 'Email 1 (Ej: mail@dominio.com)'}),
            'Email_2': TextInput(attrs={'class':'form-control fields_margin',
                                        'placeholder': 'Email 2 (Ej: mail@dominio.com)'}),
            'Rif': TextInput(attrs={'class':'form-control fields_margin',
                                    'placeholder': 'RIF (Ej: V-123456789)'}),
        }


class EstacionamientoExtendedForm(ModelForm):
    class Meta:
        model = Estacionamiento
        fields = ['NroPuesto', 'Apertura', 'Cierre']
        widgets = {
                   'NroPuesto': TextInput(attrs={'class':'form-control fields_margin',
                                                 'placeholder':'Número de Puestos (Ej: 10)'}),
                   'Apertura': TextInput(attrs={'class':'form-control fields_margin',
                                                'placeholder':'Hora de Apertura (Ej: 5:00)'}),
                   'Cierre': TextInput(attrs={'class':'form-control fields_margin',
                                              'placeholder':'Hora de Cierre (Ej: 18:00)'}),
                   }



class EsquemaTarifarioForm(ModelForm):
    class Meta:
        model = EsquemaTarifario
        fields = ['TipoEsquema', 'Tarifa']
        widgets = {
            'TipoEsquema': Select(choices=SCHEME_Choices, 
                                    attrs={'class':'form-control fields_margin'}),
            'Tarifa': TextInput(attrs={'class':'form-control fields_margin',
                                       'placeholder': 'Tarifa (Ej: 100)'}),
        }
        
        
        
class EsquemaDiferenciadoForm(ModelForm):
    class Meta:
        model = EsquemaDiferenciado
        fields = ['HoraPicoInicio', 'HoraPicoFin', 'TarifaPico']
        widgets = {
                   'HoraPicoInicio': TextInput(attrs={'class':'form-control fields_margin',
                                                      'placeholder': 'Hora Pico Inicio (Ej: 15:00)'}),
                   'HoraPicoFin': TextInput(attrs={'class':'form-control fields_margin',
                                                   'placeholder': 'Hora Pico Fin (Ej: 18:00)'}),
                   'TarifaPico': TextInput(attrs={'class':'form-control fields_margin',
                                                  'placeholder': 'Tarifa Pico (Ej: 100)'}),
                  }
        


class EstacionamientoReserva(ModelForm):
    class Meta:
        model = Reserva
        fields = ['FechaInicio', 'HoraInicio', 'FechaFinal', 'HoraFinal']
        widgets = {
            'FechaInicio': DateInput(attrs={'class':'datepicker form-control fields_margin',
                                            'placeholder': 'Fecha inicial de reserva'}),
            'FechaFinal': DateInput(attrs={'class':'datepicker form-control fields_margin',
                                           'placeholder': 'Fecha final de reserva'}),
            'HoraInicio': TextInput(attrs={'class':'form-control fields_margin',
                                           'placeholder': 'Hora inicial de reserva'}),
            'HoraFinal': TextInput(attrs={'class':'form-control fields_margin',
                                          'placeholder': 'Hora final de reserva'}),
        }

        

class PagarReservaForm(ModelForm):
    class Meta:
        model = Pago
        fields = ['NroTarjeta', 'ProveedorCred', 'CedulaTitular', 'NombreTitular']
        widgets = {
            'ProveedorCred': Select(choices=PROVCRED_Choices, 
                                    attrs={'class':'form-control fields_margin'}),
            'NroTarjeta': DateInput(attrs={'class':'form-control fields_margin',
                                           'placeholder': 'Tarjeta de Crédito (Ej: 1111-2222-3333-4444)'}),
            'CedulaTitular': TextInput(attrs={'class':'form-control fields_margin',
                                              'placeholder': 'Cédula Titular (Ej: V-12345678)'}),
            'NombreTitular': TextInput(attrs={'class':'form-control fields_margin',
                                              'placeholder': 'Nombre Titular (Ej: Pedro Pérez)'}),
        }


