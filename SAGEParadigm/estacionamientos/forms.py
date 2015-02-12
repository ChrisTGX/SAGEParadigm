# -*- coding: utf-8 -*-

from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Cantidad de esquemas tarifarios presentes en SAGE
CANT_ESQ_TARIFARIOS = 3


def esquema_tarifario_validator(value):
    value = int(value)
    if value < 1 or value > CANT_ESQ_TARIFARIOS:
        raise ValidationError('Solo existen %d esquemas tarifarios.' % CANT_ESQ_TARIFARIOS)


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
    global CANT_ESQ_TARIFARIOS
    esq_tarif_message = 'Solo existen ', str(CANT_ESQ_TARIFARIOS) ,' esquemas tarifarios.'

    puestos = forms.IntegerField(min_value = 0, label = 'Número de Puestos')

    tarifa_validator = RegexValidator(
                        regex = '^([0-9]+(\.[0-9]+)?)$',
                        message = 'Sólo debe contener dígitos.'
                    )
    esquema_tarifario_regex_validator = RegexValidator(
                                        regex = '[0-9]{1,3}$',
                                        message = esq_tarif_message
                                    )
    horarioin = forms.TimeField(required = True, label = 'Horario Apertura', 
                                widget=forms.TimeInput(format='%H:%M'))
    horarioout = forms.TimeField(required = True, label = 'Horario Cierre', 
                                 widget=forms.TimeInput(format='%H:%M'))

    horario_reserin = forms.TimeField(required = True, label = 'Horario Inicio Reserva')
    horario_reserout = forms.TimeField(required = True, label = 'Horario Fin Reserva')

    tarifa = forms.CharField(required = True, validators = [tarifa_validator])
    esquema_tarifario = forms.CharField(required = True, 
                                        validators = [esquema_tarifario_regex_validator,
                                                      esquema_tarifario_validator])



class EstacionamientoReserva(forms.Form):
    inicio = forms.TimeField(label = 'Horario Inicio Reserva')
    final = forms.TimeField(label = 'Horario Final Reserva')
