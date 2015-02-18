# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class EstacionamientoForm(forms.Form):
    phone_validator = RegexValidator(
                            regex = '^((0212)|(0412)|(0416)|(0414)|(0424)|(0426))-?\d{7}',
                            message = 'Debe introducir un formato válido.'
                        )

    # nombre del dueno (no se permiten digitos)
    propietario = forms.CharField(
                    required = True,
                    label = "Propietario",
                    validators = [
                          RegexValidator(
                                regex = '^[a-zA-ZáéíóúñÑÁÉÍÓÚ ]+$',
                                message = 'Sólo debe contener letras.'
                        )
                    ]
                )

    nombre = forms.CharField(required = True, label = "Nombre")

    direccion = forms.CharField(required = True)

    telefono_1 = forms.CharField(required = False, validators = [phone_validator])
    telefono_2 = forms.CharField(required = False, validators = [phone_validator])
    telefono_3 = forms.CharField(required = False, validators = [phone_validator])

    email_1 = forms.EmailField(required = False)
    email_2 = forms.EmailField(required = False)

    rif = forms.CharField(
                    required = True,
                    label = "RIF",
                    validators = [
                          RegexValidator(
                                regex = '^[JVD]-?\d{8}-?\d$',
                                message = 'Introduzca un RIF con un formato válido.'
                        )
                    ]
                )



class EstacionamientoExtendedForm(forms.Form):
    puestos = forms.IntegerField(required = False, min_value = 0, label = 'Número de Puestos')

    tarifa_validator = RegexValidator(
                        regex = '^([0-9]+(\.[0-9]+)?)$',
                        message = 'Sólo debe contener dígitos.'
                    )
    
    horarioin = forms.TimeField(required = False, label = 'Horario Apertura', 
                                widget=forms.TimeInput(format='%H:%M'))
    horarioout = forms.TimeField(required = False, label = 'Horario Cierre', 
                                 widget=forms.TimeInput(format='%H:%M'))

    horario_reserin = forms.TimeField(required = False, label = 'Horario Inicio Reserva')
    horario_reserout = forms.TimeField(required = False, label = 'Horario Fin Reserva')
    
    esquema_tarifario = forms.ChoiceField(required = False,
                                          choices=[(1, "Por hora"), 
                                                   (2, "Por hora y fracción"), 
                                                   (3, "Por minuto"),
                                                   (4, "Diferenciado por hora")]
                                          )
    
    tarifa = forms.DecimalField(required = False, max_digits=6, decimal_places=2)



class EstacionamientoReserva(forms.Form):
    inicio = forms.TimeField(label = 'Horario Inicio Reserva')
    final = forms.TimeField(label = 'Horario Final Reserva')



class PagarReservaForm(forms.form):
    nro_tarjeta_credito = forms.CharField(
                            required = True,
                            label = "Tarjeta de crédito",
                            validators = [
                                          RegexValidator(
                                                regex = '^\d{16}$',
                                                message = 'Introduzca un número de tarjeta de crédito con un formato válido.'
                                                )
                                          ]
                            )
    proveedor_credito = forms.ChoiceField(required = False,
                                          choices=[(1, "Vista"), 
                                                   (2, "Mister"), 
                                                   (3, "Xpres")]
                                          )
    

