# -*- coding: utf-8 -*-

import datetime
from django.test import Client
from django.test import TestCase
import unittest

from estacionamientos.controller import *
from estacionamientos.forms import *


###################################################################
#                    ESTACIONAMIENTO VISTA DISPONIBLE
###################################################################
class SimpleTest(unittest.TestCase):
    # normal
    def setUp(self):
        self.client = Client()

    # normal
    def test_primera(self):
        response = self.client.get('/estacionamientos/')
        self.assertEqual(response.status_code, 200)



###################################################################
#                    ESTACIONAMIENTO_ALL FORM
###################################################################

class SimpleFormTestCase(TestCase):

    # malicia
    def test_CamposVacios(self):
        form_data = {}
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_SoloUnCampoNecesario(self):
        form_data = {
            'propietario': 'Pedro'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_DosCamposNecesarios(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_TresCamposNecesarios(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_TodosLosCamposNecesarios(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_PropietarioInvalidoDigitos(self):
        form_data = {
            'propietario': 'Pedro132',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_PropietarioInvalidoSimbolos(self):
        form_data = {
            'propietario': 'Pedro!',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_RIFtamanoinvalido(self):
        form_data = {
            'propietario': 'Pedro132',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V1234567'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_RIFformatoinvalido(self):
        form_data = {
            'propietario': 'Pedro132',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'Kaa123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_AgregarTLFs(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V123456789',
            'telefono_1': '02129322878',
            'telefono_2': '04149322878',
            'telefono_3': '04129322878'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_FormatoInvalidoTLF(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V123456789',
            'telefono_1': '02119322878'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_TamanoInvalidoTLF(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V123456789',
            'telefono_1': '0219322878'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_AgregarCorreos(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V123456789',
            'telefono_1': '02129322878',
            'telefono_2': '04149322878',
            'telefono_3': '04129322878',
            'email_1': 'adminsitrador@admin.com',
            'email_2': 'usua_rio@users.com'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_CorreoInvalido(self):
        form_data = {
            'propietario': 'Pedro',
            'nombre': 'Orinoco',
            'direccion': 'Caracas',
            'rif': 'V123456789',
            'telefono_1': '02129322878',
            'telefono_2': '04149322878',
            'telefono_3': '04129322878',
            'email_1': 'adminsitrador@a@dmin.com'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

###################################################################
# ESTACIONAMIENTO_EXTENDED_FORM
###################################################################

    # malicia
    def test_EstacionamientoExtendedForm_UnCampo(self):
        form_data = { 'puestos': 2}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_DosCampos(self):
        form_data = { 'puestos': 2,
                                'horarioin': datetime.time(6, 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_TresCampos(self):
        form_data = { 'puestos': 2,
                                'horarioin': datetime.time(6, 0),
                                'horarioout': datetime.time(19, 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_CuatroCampos(self):
        form_data = { 'puestos': 2,
                                'horarioin': datetime.time(6, 0),
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': datetime.time(7, 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_EstacionamientoExtendedForm_CincoCampos(self):
        form_data = { 'puestos': 2,
                                'horarioin': datetime.time(6, 0),
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': datetime.time(7, 0),
                                'horario_reserout': datetime.time(14, 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_EstacionamientoExtendedForm_TodosCamposBien(self):
        form_data = { 'puestos': 2,
                                'horarioin': datetime.time(6, 0),
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': datetime.time(7, 0),
                                'horario_reserout': datetime.time(14, 0),
                                'tarifa': '12',
                                'esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # caso borde
    def test_EstacionamientoExtendedForm_Puestos0(self):
        form_data = { 'puestos': 0,
                                'horarioin': datetime.time(6, 0),
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': datetime.time(7, 0),
                                'horario_reserout': datetime.time(14, 0),
                                'tarifa': '12',
                                'esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # caso borde
    def test_EstacionamientoExtendedForm_HoraInicioIgualHoraCierre(self):
        form_data = { 'puestos': 2,
                                'horarioin': datetime.time(6, 0),
                                'horarioout': datetime.time(6, 0),
                                'horario_reserin': datetime.time(7, 0),
                                'horario_reserout': datetime.time(14, 0),
                                'tarifa': '12',
                                'esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # caso borde
    def test_EstacionamientoExtendedForm_HoraIniReserIgualHoraFinReser(self):
        form_data = { 'puestos': 2,
                                'horarioin': datetime.time(6, 0),
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': datetime.time(7, 0),
                                'horario_reserout': datetime.time(7, 0),
                                'tarifa': '12',
                                'esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True) 

    # malicia
    def test_EstacionamientoExtendedForm_StringEnPuesto(self):
        form_data = { 'puestos': 'hola',
                                'horarioin': datetime.time(6, 0),
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': datetime.time(7, 0),
                                'horario_reserout': datetime.time(14, 0),
                                'tarifa': '12',
                                'esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_StringHoraInicio(self):
        form_data = { 'puestos': 2,
                                'horarioin': 'holaa',
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': datetime.time(7, 0),
                                'horario_reserout': datetime.time(14, 0),
                                'tarifa': '12',
                                'esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_NumeroNegativoHoraInicio(self):
        form_data = { 'puestos': 2,
                                'horarioin':-1,
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': datetime.time(7, 0),
                                'horario_reserout': datetime.time(14, 0),
                                'tarifa': '12',
                                'esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_NoneEntarifa(self):
        form_data = { 'puestos': 2,
                                'horarioin': datetime.time(6, 0),
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': datetime.time(7, 0),
                                'horario_reserout': datetime.time(14, 0),
                                'tarifa': None}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_NoneEnHorarioReserva(self):
        form_data = { 'puestos': 2,
                                'horarioin': 'holaa',
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': None,
                                'horario_reserout': datetime.time(14, 0),
                                'tarifa': '12'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_listaEnHoraReserva(self):
        form_data = { 'puestos': 2,
                                'horarioin': datetime.time(6, 0),
                                'horarioout': datetime.time(19, 0),
                                'horario_reserin': datetime.time(7, 0),
                                'horario_reserout': [datetime.time(14, 0)],
                                'tarifa': 12}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

######################################################################
# ESTACIONAMIENTO_EXTENDED pruebas controlador
###################################################################

    # normal
    def test_HorariosValidos(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 18, minute = 0, second = 0)
        ReservaInicio = datetime.time(hour = 12, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 18, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (True, ''))

    # malicia
    def test_HorariosInvalido_HoraCierre_Menor_HoraApertura(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 11, minute = 0, second = 0)
        ReservaInicio = datetime.time(hour = 12, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 18, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (False, 'El horario de apertura debe ser menor al horario de cierre'))

    # caso borde
    def test_HorariosInvalido_HoraCierre_Igual_HoraApertura(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 12, minute = 0, second = 0)
        ReservaInicio = datetime.time(hour = 12, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 18, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (False, 'El horario de apertura debe ser menor al horario de cierre'))

    # caso borde
    def test_HorariosInvalido_HoraCierreReserva_Menor_HoraAperturaReserva(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 18, minute = 0, second = 0)
        ReservaInicio = datetime.time(hour = 12, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 11, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (False, 'El horario de inicio de reserva debe ser menor al horario de cierre'))

    # caso borde
    def test_HorariosInvalido_HoraCierreReserva_Igual_HoraAperturaReserva(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 18, minute = 0, second = 0)
        ReservaInicio = datetime.time(hour = 12, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 12, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (False, 'El horario de inicio de reserva debe ser menor al horario de cierre'))

    # caso borde
    def test_Limite_HorarioValido_Apertura_Cierre(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 12, minute = 0, second = 1)
        ReservaInicio = datetime.time(hour = 12, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 12, minute = 0, second = 1)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (True, ''))

    # caso borde
    def test_Limite_Superior_HorarioValido_Apertura_Cierre(self):
        HoraInicio = datetime.time(hour = 0, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 23, minute = 59, second = 59)
        ReservaInicio = datetime.time(hour = 12, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 23, minute = 59, second = 59)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (True, ''))

    # caso borde
    def test_InicioReserva_Mayor_HoraCierreEstacionamiento(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 18, minute = 0, second = 0)
        ReservaInicio = datetime.time(hour = 19, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 20, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (False, 'El horario de comienzo de reserva debe ser menor al horario de cierre del estacionamiento'))

    # caso borde
    def test_InicioReserva_Mayor_HoraCierreEstacionamiento2(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 18, minute = 0, second = 0)
        ReservaInicio = datetime.time(hour = 19, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 20, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (False, 'El horario de comienzo de reserva debe ser menor al horario de cierre del estacionamiento'))

    # malicia
    def test_CierreReserva_Mayor_HoraCierreEstacionamiento(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 18, minute = 0, second = 0)
        ReservaInicio = datetime.time(hour = 17, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 20, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (False, 'El horario de cierre de estacionamiento debe ser mayor o igual al horario de finalización de reservas'))

    # malicia
    def test_CierreReserva_Menos_HoraInicioEstacionamiento(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 18, minute = 0, second = 0)
        ReservaInicio = datetime.time(hour = 10, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 11, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin)
        self.assertEqual(x, (False, 'El horario de inicio de reserva debe ser mayor o igual al horario de apertura del estacionamiento'))



###################################################################
# ESTACIONAMIENTO_RESERVA_FORM
###################################################################

    # malicia
    def test_EstacionamientoReserva_Vacio(self):
        form_data = {}
        form = EstacionamientoReserva(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_EstacionamientoReserva_UnCampo(self):
        form_data = {'inicio':datetime.time(6, 0)}
        form = EstacionamientoReserva(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # normal
    def test_EstacionamientoReserva_TodosCamposBien(self):
        form_data = {'inicio':datetime.time(6, 0), 'final':datetime.time(12, 0)}
        form = EstacionamientoReserva(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_EstacionamientoReserva_InicioString(self):
        form_data = {'inicio':'hola',
                                'final':datetime.time(12, 0)}
        form = EstacionamientoReserva(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoReserva_FinString(self):
        form_data = {'inicio':datetime.time(6, 0),
                                'final':'hola'}
        form = EstacionamientoReserva(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoReserva_InicioNone(self):
        form_data = {'inicio':None,
                                'final':datetime.time(12, 0)}
        form = EstacionamientoReserva(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoReserva_finalNone(self):
        form_data = {'inicio':datetime.time(6, 0),
                                'final':None}
        form = EstacionamientoReserva(data = form_data)
        self.assertEqual(form.is_valid(), False)

###################################################################
# PRUEBAS DE FUNCIONES DEL CONTROLADOR
###################################################################

##############################################################
# Estacionamiento Reserva Controlador
###################################################################

# HorarioReserva, pruebas Unitarias

    # normal
    def test_HorarioReservaValido(self):
        ReservaInicio = datetime.time(hour = 13, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 15, minute = 0, second = 0)
        HoraApertura = datetime.time(hour = 12, minute = 0, second = 0)
        HoraCierre = datetime.time(hour = 18, minute = 0, second = 0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (True, ''))

    # caso borde
    def test_HorarioReservaInvalido_InicioReservacion_Mayor_FinalReservacion(self):
        ReservaInicio = datetime.time(hour = 13, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 12, minute = 59, second = 59)
        HoraApertura = datetime.time(hour = 12, minute = 0, second = 0)
        HoraCierre = datetime.time(hour = 18, minute = 0, second = 0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El horario de apertura debe ser menor al horario de cierre'))

    # caso borde
    def test_HorarioReservaInvalido_TiempoTotalMenor1h(self):
        ReservaInicio = datetime.time(hour = 13, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 13, minute = 59, second = 59)
        HoraApertura = datetime.time(hour = 12, minute = 0, second = 0)
        HoraCierre = datetime.time(hour = 18, minute = 0, second = 0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El tiempo de reserva debe ser al menos de 1 hora'))

    # caso borde
    def test_HorarioReservaInvalido_ReservaFinal_Mayor_HorarioCierre(self):
        ReservaInicio = datetime.time(hour = 13, minute = 0, second = 0)
        ReservaFin = datetime.time(hour = 18, minute = 0, second = 1)
        HoraApertura = datetime.time(hour = 12, minute = 0, second = 0)
        HoraCierre = datetime.time(hour = 18, minute = 0, second = 0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El horario de inicio de reserva debe estar en un horario válido'))

    # caso borde
    def test_HorarioReservaInvalido_ReservaInicial_Menor_HorarioApertura(self):
        ReservaInicio = datetime.time(hour = 11, minute = 59, second = 59)
        ReservaFin = datetime.time(hour = 15, minute = 0, second = 1)
        HoraApertura = datetime.time(hour = 12, minute = 0, second = 0)
        HoraCierre = datetime.time(hour = 18, minute = 0, second = 0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El horario de cierre de reserva debe estar en un horario válido'))

    # malicia
    def test_Reservacion_CamposVacios(self):
        form_data = {'inicio':datetime.time(6, 0), 'final':datetime.time(12, 0)}
        form = EstacionamientoReserva(data = form_data)
        self.assertEqual(form.is_valid(), True)

# Binaria, Pruebas Unitarias

    # caso borde
    def test_Binaria_lista_vacia(self):
        valor = datetime.time(hour = 10, minute = 0, second = 0)
        lista = []
        x = binaria(valor, 0, len(lista), lista)
        self.assertEqual(x, 0)

    # caso borde
    def test_Binaria_lista_un_elem(self):
        valor = datetime.time(hour = 10, minute = 0, second = 0)
        Hora1In = datetime.time(hour = 8, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 9, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        x = binaria(valor, 0, len(lista), lista)
        self.assertEqual(x, 1)

    # caso borde
    def test_Binaria_horas_borde(self):
        valor = datetime.time(hour = 10, minute = 0, second = 0)
        Hora1In = datetime.time(hour = 0, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 0, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 23, minute = 59, second = 59)
        Hora2Out = datetime.time(hour = 23, minute = 59, second = 59)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        x = binaria(valor, 0, len(lista), lista)
        self.assertEqual(x, 1)

    # caso borde
    def test_Binaria_horas_borde2(self):
        valor = datetime.time(hour = 0, minute = 0, second = 0)
        Hora1In = datetime.time(hour = 0, minute = 0, second = 1)
        Hora1Out = datetime.time(hour = 0, minute = 0, second = 1)
        Hora2In = datetime.time(hour = 23, minute = 59, second = 59)
        Hora2Out = datetime.time(hour = 23, minute = 59, second = 59)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        x = binaria(valor, 0, len(lista), lista)
        self.assertEqual(x, 0)

    # caso borde
    def test_Binaria_horas_borde3(self):
        valor = datetime.time(hour = 23, minute = 59, second = 59)
        Hora1In = datetime.time(hour = 0, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 0, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 23, minute = 59, second = 58)
        Hora2Out = datetime.time(hour = 23, minute = 59, second = 58)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        x = binaria(valor, 0, len(lista), lista)
        self.assertEqual(x, 2)

    # malicia
    def test_Binaria_horas_mal_orden(self):
        valor = datetime.time(hour = 20, minute = 10, second = 13)
        Hora1In = datetime.time(hour = 0, minute = 1, second = 0)
        Hora1Out = datetime.time(hour = 0, minute = 0, second = 30)
        Hora2In = datetime.time(hour = 23, minute = 59, second = 59)
        Hora2Out = datetime.time(hour = 23, minute = 59, second = 58)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        x = binaria(valor, 0, len(lista), lista)
        self.assertEqual(x, 1)

    # malicia
    def test_Binaria_horas_mal_orden2(self):
        valor = datetime.time(hour = 20, minute = 10, second = 13)
        Hora1In = datetime.time(hour = 0, minute = 1, second = 0)
        Hora1Out = datetime.time(hour = 0, minute = 0, second = 30)
        Hora2In = datetime.time(hour = 23, minute = 59, second = 59)
        Hora2Out = datetime.time(hour = 19, minute = 59, second = 58)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        x = binaria(valor, 0, len(lista), lista)
        self.assertEqual(x, 1)

    # malicia
    def test_Binaria_horas_mal_orden3(self):
        valor = datetime.time(hour = 20, minute = 10, second = 13)
        Hora1In = datetime.time(hour = 0, minute = 1, second = 0)
        Hora1Out = datetime.time(hour = 0, minute = 0, second = 30)
        Hora2In = datetime.time(hour = 23, minute = 59, second = 59)
        Hora2Out = datetime.time(hour = 19, minute = 59, second = 58)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        x = binaria(valor, 0, len(lista), lista)
        self.assertEqual(x, 1)

# busquedaBin, Pruebas Integracion, funcion 'binaria' con 'busquedaBin'

    # caso borde
    def test_BusquedaBin_horarios_todoeldia(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 22, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (1, True))

    # caso borde
    def test_BusquedaBin_noDisponible(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora3In, Hora3Out])
        lista.append([Hora2In, Hora2Out])
        HoraIn = datetime.time(hour = 7, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 9, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (2, False))

    # normal
    def test_BusquedaBin_noDisponible_reservarTodoElDia(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora3In, Hora3Out])
        lista.append([Hora2In, Hora2Out])
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 22, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (1, False))

    # caso borde
    def test_BusquedaBin_lista_solo_maxmin(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        HoraIn = datetime.time(hour = 12, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 18, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (1, True))

    # caso borde
    def test_BusquedaBin_horasIguales_Inicio(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 6, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (1, True))

    # caso borde
    def test_BusquedaBin_horasIguales_Fin(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        HoraIn = datetime.time(hour = 22, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 22, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (1, True))

    # malicia
    def test_BusquedaBin_lista_no_inicializada(self):
        lista = []
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 12, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (0, True))

    # malicia
    def test_BusquedaBin_lista_None(self):
        lista = None
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 12, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (0, False))

    # malicia
    def test_BusquedaBin_lista_noLista(self):
        lista = 'String'
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 12, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (0, False))

    # malicia
    def test_BusquedaBin_horaIngreso_None(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        HoraIn = None
        HoraOut = datetime.time(hour = 22, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (0, False))

    # malicia
    def test_BusquedaBin_horaSalida_None(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = None
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (0, False))

    # malicia
    def test_BusquedaBin_horaIngreso_no_datetime(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        HoraIn = 'String'
        HoraOut = datetime.time(hour = 22, minute = 0, second = 0)
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (0, False))

    # malicia
    def test_BusquedaBin_horaSalida_no_datetime(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = 'String'
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (0, False))

    # normal
    def test_BusquedaBin_todoEn_None(self):
        lista = None
        HoraIn = None
        HoraOut = None
        x = busquedaBin(HoraIn, HoraOut, lista)
        self.assertEqual(x, (0, False))

# buscar, Pruebas Integracion, funcion 'busquedaBin' con 'buscar'

    # normal
    def test_buscar_funcionalidadOK(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        estacionamiento = [lista for _ in range(2)]
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 12, minute = 0, second = 0)
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (0, 1, True))

    # caso borde
    def test_buscar_horas_Iguales(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora2In, Hora2Out])
        estacionamiento = [lista for _ in range(2)]
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 6, minute = 0, second = 0)
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (0, 1, True))

    # caso borde
    def test_buscar_estacionamientoLleno(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora3In, Hora3Out])
        lista.append([Hora2In, Hora2Out])
        estacionamiento = [lista for _ in range(2)]
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 12, minute = 0, second = 0)
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (-1, -1, False))

    # malicia
    def test_buscar_estacionamiento_None(self):
        estacionamiento = None
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 12, minute = 0, second = 0)
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (-1, -1, False))

    # malicia
    def test_buscar_estacionamiento_noLista(self):
        estacionamiento = 'String'
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 12, minute = 0, second = 0)
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (-1, -1, False))

    # malicia
    def test_buscar_estacionamiento_noInicializado(self):
        estacionamiento = []
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = datetime.time(hour = 12, minute = 0, second = 0)
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (-1, -1, False))

    # malicia
    def test_buscar_horaIngreso_None(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora3In, Hora3Out])
        lista.append([Hora2In, Hora2Out])
        estacionamiento = [lista for _ in range(2)]
        HoraIn = None
        HoraOut = datetime.time(hour = 12, minute = 0, second = 0)
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (-1, -1, False))

    # malicia
    def test_buscar_horaFin_None(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora3In, Hora3Out])
        lista.append([Hora2In, Hora2Out])
        estacionamiento = [lista for _ in range(2)]
        HoraIn = datetime.time(hour = 6, minute = 0, second = 0)
        HoraOut = None
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (-1, -1, False))

    # malicia
    def test_buscar_horaIngreso_noDatetime(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append([Hora1In, Hora1Out])
        lista.append([Hora3In, Hora3Out])
        lista.append([Hora2In, Hora2Out])
        estacionamiento = [lista for _ in range(2)]
        HoraIn = 'String'
        HoraOut = datetime.time(hour = 12, minute = 0, second = 0)
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (-1, -1, False))

    # normal
    def test_buscar_todo_None(self):
        estacionamiento = None
        HoraIn = None
        HoraOut = None
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (-1, -1, False))

    # normal
    def test_buscar_todo_invalido(self):
        estacionamiento = 'String'
        HoraIn = 42
        HoraOut = 42
        x = buscar(HoraIn, HoraOut, estacionamiento)
        self.assertEqual(x, (-1, -1, False))


# insertarReserva, Pruebas Unitarias
# no se requiere unas pruebas exaustivas de esta funcion, ya que esta funcion
# solo agrega una tupla a la lista otorgada utilizando la funcion 'insert' de las listas
# de python, la cual presumo que ha sido probada en gran cantidad de oportunidades

    # normal
    def test_insertarReserva_funcionalidadOk(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        lista2 = []
        lista2.append((Hora1In, Hora1Out))
        lista2.append((Hora3In, Hora3Out))
        lista2.append((Hora2In, Hora2Out))
        x = insertarReserva(Hora3In, Hora3Out, 1, lista)
        self.assertEqual(x, lista2)

    # malicia
    def test_insertarReserva_lista_None(self):
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = None
        x = insertarReserva(Hora3In, Hora3Out, 1, lista)
        self.assertEqual(x, None)

    # malicia
    def test_insertarReserva_lista_noLista(self):
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = 'String'
        x = insertarReserva(Hora3In, Hora3Out, 1, lista)
        self.assertEqual(x, None)

    # malicia
    def test_insertarReserva_horaIngreso_None(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = None
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        x = insertarReserva(Hora3In, Hora3Out, 1, lista)
        self.assertEqual(x, lista)

    # malicia
    def test_insertarReserva_horaSalida_None(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = None
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        x = insertarReserva(Hora3In, Hora3Out, 1, lista)
        self.assertEqual(x, lista)

    # malicia
    def test_insertarReserva_horaIngreso_noDatetime(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = 42
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        x = insertarReserva(Hora3In, Hora3Out, 1, lista)
        self.assertEqual(x, lista)

    # malicia
    def test_insertarReserva_horaSalida_noDatetime(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = 42
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        x = insertarReserva(Hora3In, Hora3Out, 1, lista)
        self.assertEqual(x, lista)

    # malicia
    def test_insertarReserva_todo_None(self):
        lista = None
        x = insertarReserva(None, None, 1, lista)
        self.assertEqual(x, None)

# reservar, Pruebas Integracion, funciones 'reservar', 'buscar' e 'insertarReserva'

    # normal
    def test_reservar_funcionalidadOk(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 8, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 12, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        estacionamiento = [lista for _ in range(2)]
        lista2 = []
        lista2.append((Hora1In, Hora1Out))
        lista2.append((Hora3In, Hora3Out))
        lista2.append((Hora2In, Hora2Out))
        estacionamiento2 = []
        estacionamiento2.append(lista2)
        estacionamiento2.append(lista)
        x = reservar(Hora3In, Hora3Out, estacionamiento)
        self.assertEqual(x, estacionamiento2)

    # caso frontera
    def test_reservar_estacionamiento_full(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora3In, Hora3Out))
        lista.append((Hora2In, Hora2Out))
        estacionamiento = [lista for _ in range(2)]
        x = reservar(Hora3In, Hora3Out, estacionamiento)
        self.assertEqual(x, 1)

    # caso frontera
    def test_reservar_ultimoPuestoAReservar(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 8, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 12, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        lista2 = []
        lista2.append((Hora1In, Hora1Out))
        lista2.append((Hora3In, Hora3Out))
        lista2.append((Hora2In, Hora2Out))
        estacionamiento = []
        estacionamiento.append(lista2)
        estacionamiento.append(lista)
        estacionamiento2 = []
        estacionamiento2.append(lista2)
        estacionamiento2.append(lista2)
        x = reservar(Hora3In, Hora3Out, estacionamiento)
        self.assertEqual(x, estacionamiento2)

    # malicia
    def test_reservar_estacionamiento_None(self):
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        estacionamiento = None
        x = reservar(Hora3In, Hora3Out, estacionamiento)
        self.assertEqual(x, 1)

    # malicia
    def test_reservar_estacionamiento_noLista(self):
        Hora3In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3Out = datetime.time(hour = 22, minute = 0, second = 0)
        estacionamiento = 'String'
        x = reservar(Hora3In, Hora3Out, estacionamiento)
        self.assertEqual(x, 1)

    # malicia
    def test_reservar_horaIngreso_None(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = None
        Hora3Out = datetime.time(hour = 12, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        estacionamiento = [lista for _ in range(2)]
        lista2 = []
        lista2.append((Hora1In, Hora1Out))
        lista2.append((Hora3In, Hora3Out))
        lista2.append((Hora2In, Hora2Out))
        estacionamiento2 = []
        estacionamiento2.append(lista2)
        estacionamiento2.append(lista)
        x = reservar(Hora3In, Hora3Out, estacionamiento)
        self.assertEqual(x, 1)

    # malicia
    def test_reservar_horaSalida_None(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 8, minute = 0, second = 0)
        Hora3Out = None
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        estacionamiento = [lista for _ in range(2)]
        lista2 = []
        lista2.append((Hora1In, Hora1Out))
        lista2.append((Hora3In, Hora3Out))
        lista2.append((Hora2In, Hora2Out))
        estacionamiento2 = []
        estacionamiento2.append(lista2)
        estacionamiento2.append(lista)
        x = reservar(Hora3In, Hora3Out, estacionamiento)
        self.assertEqual(x, 1)

    # malicia
    def test_reservar_horaIngreso_noLista(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = 'String'
        Hora3Out = datetime.time(hour = 12, minute = 0, second = 0)
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        estacionamiento = [lista for _ in range(2)]
        lista2 = []
        lista2.append((Hora1In, Hora1Out))
        lista2.append((Hora3In, Hora3Out))
        lista2.append((Hora2In, Hora2Out))
        estacionamiento2 = []
        estacionamiento2.append(lista2)
        estacionamiento2.append(lista)
        x = reservar(Hora3In, Hora3Out, estacionamiento)
        self.assertEqual(x, 1)

    # malicia
    def test_reservar_horaSalida_noLista(self):
        Hora1In = datetime.time(hour = 6, minute = 0, second = 0)
        Hora1Out = datetime.time(hour = 6, minute = 0, second = 0)
        Hora3In = datetime.time(hour = 8, minute = 0, second = 0)
        Hora3Out = 'String'
        Hora2In = datetime.time(hour = 22, minute = 0, second = 0)
        Hora2Out = datetime.time(hour = 22, minute = 0, second = 0)
        lista = []
        lista.append((Hora1In, Hora1Out))
        lista.append((Hora2In, Hora2Out))
        estacionamiento = [lista for _ in range(2)]
        lista2 = []
        lista2.append((Hora1In, Hora1Out))
        lista2.append((Hora3In, Hora3Out))
        lista2.append((Hora2In, Hora2Out))
        estacionamiento2 = []
        estacionamiento2.append(lista2)
        estacionamiento2.append(lista)
        x = reservar(Hora3In, Hora3Out, estacionamiento)
        self.assertEqual(x, 1)

    # malicia
    def test_reservar_todo_None(self):
        x = reservar(None, None, None)
        self.assertEqual(x, 1)
        
    
class EsquemasTarifariosTests(unittest.TestCase):
    def testcostoHorasCompletas(self):
        self.assertEqual(costoHorasCompletas(4,5),20)

    def testcostoFraccionHoraEsquema1(self):
        self.assertEqual(costoFraccionHoraEsquema1(0, 0), 0)
        self.assertEqual(costoFraccionHoraEsquema1(0, 5), 0)
        self.assertEqual(costoFraccionHoraEsquema1(5, 0), 0)    
        
        self.assertEqual(costoFraccionHoraEsquema1(0.01, 0), 0)
        self.assertEqual(costoFraccionHoraEsquema1(0.01, 5), 5)
        self.assertEqual(costoFraccionHoraEsquema1(5, 0.01), 0.01) 
        
    def testcostoFraccionHoraEsquema2(self):
        # si la fraccion es igual a 0
        self.assertEqual(costoFraccionHoraEsquema2(0, 0), 0)
        self.assertEqual(costoFraccionHoraEsquema2(0, 5), 0)   
        
        self.assertEqual(costoFraccionHoraEsquema2(0.01, 0), 0)
        self.assertEqual(costoFraccionHoraEsquema2(0.01, 5), 2.5)   
        # si la fraccion es menor o igual que 30
        
        self.assertEqual(costoFraccionHoraEsquema2(25, 0), 0) 
        self.assertEqual(costoFraccionHoraEsquema2(25, 5), 2.5) 
        
        self.assertEqual(costoFraccionHoraEsquema2(29.9, 0), 0) 
        self.assertEqual(costoFraccionHoraEsquema2(29.9, 5), 2.5) 
        
        self.assertEqual(costoFraccionHoraEsquema2(30, 0), 0)
        self.assertEqual(costoFraccionHoraEsquema2(30, 10), 5)
        
        self.assertEqual(costoFraccionHoraEsquema2(30.01, 0), 0)
        self.assertEqual(costoFraccionHoraEsquema2(30.01, 10), 10)
                  
    def testcostoFraccionHoraEsquema3(self):
        #si la fraccion es igual a 0
        self.assertEqual(costoFraccionHoraEsquema3(0, 0), 0)
        self.assertEqual(costoFraccionHoraEsquema3(0, 5), 0)
        self.assertEqual(costoFraccionHoraEsquema3(5, 0), 0)
        
        self.assertEqual(costoFraccionHoraEsquema3(0.01, 0), 0)
        self.assertEqual(costoFraccionHoraEsquema3(0.01, 5), 0.01*(5/60))
        self.assertEqual(costoFraccionHoraEsquema3(5, 0.01), 5*(0.01/60))
        #si la fraccion es diferente a 0
        
        self.assertEqual(costoFraccionHoraEsquema3(10, 120), 20)
