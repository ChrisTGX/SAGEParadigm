# -*- coding: utf-8 -*-

import datetime
from django.test import Client
from django.test import TestCase
import unittest

from estacionamientos.controller import *
from estacionamientos.forms import *
#from __builtin__ import *


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
            'Propietario': 'Pedro'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_DosCamposNecesarios(self):
        form_data = {
            'Propietario': 'Pedro',
            'Nombre': 'Orinoco'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_TresCamposNecesarios(self):
        form_data = {
            'Propietario': 'Pedro',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # caso borde
    def test_TodosLosCamposNecesarios(self):
        form_data = {
            'Propietario': 'Pedro',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas',
            'Rif': 'V123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_PropietarioInvalidoDigitos(self):
        form_data = {
            'Propietario': 'Pedro132',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas',
            'Rif': 'V123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_PropietarioInvalidoSimbolos(self):
        form_data = {
            'Propietario': 'Pedro!',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas',
            'Rif': 'V123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_RIFtamanoinvalido(self):
        form_data = {
            'Propietario': 'Pedro132',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas',
            'Rif': 'V1234567'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_RIFformatoinvalido(self):
        form_data = {
            'Propietario': 'Pedro132',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas',
            'Rif': 'Kaa123456789'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_AgregarTLFs(self):
        form_data = {
            'Propietario': 'Pedro',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas',
            'Rif': 'V123456789',
            'Telefono_1': '02129322878',
            'Telefono_2': '04149322878',
            'Telefono_3': '04129322878'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_FormatoInvalidoTLF(self):
        form_data = {
            'Propietario': 'Pedro',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas',
            'Rif': 'V123456789',
            'Telefono_1': '02119322878'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # caso borde
    def test_TamanoInvalidoTLF(self):
        form_data = {
            'Propietario': 'Pedro',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas',
            'Rif': 'V123456789',
            'Telefono_1': '0219322878'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_AgregarCorreos(self):
        form_data = {
            'Propietario': 'Pedro',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas',
            'Rif': 'V123456789',
            'Telefono_1': '02129322878',
            'Telefono_2': '04149322878',
            'Telefono_3': '04129322878',
            'Email_1': 'adminsitrador@admin.com',
            'Email_2': 'usua_rio@users.com'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_CorreoInvalido(self):
        form_data = {
            'Propietario': 'Pedro',
            'Nombre': 'Orinoco',
            'Direccion': 'Caracas',
            'Rif': 'V123456789',
            'Telefono_1': '02129322878',
            'Telefono_2': '04149322878',
            'Telefono_3': '04129322878',
            'Email_1': 'adminsitrador@a@dmin.com'
        }
        form = EstacionamientoForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

###################################################################
# ESTACIONAMIENTO_EXTENDED_FORM
###################################################################

    # malicia
    def test_EstacionamientoExtendedForm_UnCampoHorario(self):
        form_data = { 'Apertura': datetime.time(6, 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_EstacionamientoExtendedForm_DosCamposHorario(self):
        form_data = { 'Apertura': datetime.time(6, 0),
                      'Cierre': datetime.time(19, 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_EstacionamientoExtendedForm_TresCamposHorario(self):
        form_data = { 'Apertura': datetime.time(6, 0),
                      'Cierre': datetime.time(19, 0),
                      'Reservas_Inicio': datetime.time(7, 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # caso borde
    def test_EstacionamientoExtendedForm_CuatroCamposHorario(self):
        form_data = { 'Apertura': datetime.time(6, 0),
                      'Cierre': datetime.time(19, 0),
                      'Reservas_Inicio': datetime.time(7, 0),
                      'Reservas_Cierre': datetime.time(14, 0)}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # caso borde
    def test_EstacionamientoExtendedForm_TodosCamposBien(self):
        form_data = { 'Puestos': 2,
                                'Apertura': datetime.time(6, 0),
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': datetime.time(14, 0),
                                'Tarifa': '12',
                                'Esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # caso borde
    def test_EstacionamientoExtendedForm_Puestos0(self):
        form_data = { 'Puestos': 0,
                                'Apertura': datetime.time(6, 0),
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': datetime.time(14, 0),
                                'Tarifa': '12',
                                'Esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # caso borde
    def test_EstacionamientoExtendedForm_HoraInicioIgualHoraCierre(self):
        form_data = { 'Puestos': 2,
                                'Apertura': datetime.time(6, 0),
                                'Cierre': datetime.time(6, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': datetime.time(14, 0),
                                'Tarifa': '12',
                                'Esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # caso borde
    def test_EstacionamientoExtendedForm_HoraIniReserIgualHoraFinReser(self):
        form_data = { 'Puestos': 2,
                                'Apertura': datetime.time(6, 0),
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': datetime.time(7, 0),
                                'Tarifa': '12',
                                'Esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True) 

    def test_EstacionamientoExtendedForm_EsquemaTarifarioInexsitente(self):
        form_data = { 'Puestos': 2,
                                'Apertura': datetime.time(6, 0),
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': datetime.time(7, 0),
                                'Tarifa': '12',
                                'Esquema_tarifario': '1000000'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_StringEnPuesto(self):
        form_data = { 'Puestos': 'hola',
                                'Apertura': datetime.time(6, 0),
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': datetime.time(14, 0),
                                'Tarifa': '12',
                                'Esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_EstacionamientoExtendedForm_StringHoraInicio(self):
        form_data = { 'Puestos': 2,
                                'Apertura': 'holaa',
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': datetime.time(14, 0),
                                'Tarifa': '12',
                                'Esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_NumeroNegativoHoraInicio(self):
        form_data = { 'Puestos': 2,
                                'Apertura':-1,
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': datetime.time(14, 0),
                                'Tarifa': '12',
                                'Esquema_tarifario': '1'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_NoneEntarifa(self):
        form_data = { 'Puestos': 2,
                                'Apertura': datetime.time(6, 0),
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': datetime.time(14, 0),
                                'Tarifa': None}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)
        
    # malicia
    def test_EstacionamientoExtendedForm_NoneEsquemaTarifario(self):
        form_data = { 'Puestos': 2,
                                'Apertura': datetime.time(6, 0),
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': datetime.time(14, 0),
                                'Tarifa': '12',
                                'Esquema_tarifario':None}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_EstacionamientoExtendedForm_NoneEnHorarioReserva(self):
        form_data = { 'Puestos': 2,
                                'Apertura': 'holaa',
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': None,
                                'Reservas_Cierre': datetime.time(14, 0),
                                'Tarifa': '12'}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoExtendedForm_listaEnHoraReserva(self):
        form_data = { 'Puestos': 2,
                                'Apertura': datetime.time(6, 0),
                                'Cierre': datetime.time(19, 0),
                                'Reservas_Inicio': datetime.time(7, 0),
                                'Reservas_Cierre': [datetime.time(14, 0)],
                                'Tarifa': 12}
        form = EstacionamientoExtendedForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

######################################################################
# ESTACIONAMIENTO_EXTENDED pruebas controlador
###################################################################

    # normal
    def test_HorariosValidos(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 18, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin)
        self.assertEqual(x, (True, ''))

    # malicia
    def test_HorariosInvalido_HoraCierre_Menor_HoraApertura(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 11, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin)
        self.assertEqual(x, (False, 'El horario de apertura debe ser menor al horario de cierre'))

    # caso borde
    def test_HorariosInvalido_HoraCierre_Igual_HoraApertura(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 12, minute = 0, second = 0)
        x = HorarioEstacionamiento(HoraInicio, HoraFin)
        self.assertEqual(x, (False, 'El horario de apertura debe ser menor al horario de cierre'))

    # caso borde
    def test_Limite_HorarioValido_Apertura_Cierre(self):
        HoraInicio = datetime.time(hour = 12, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 12, minute = 0, second = 1)
        x = HorarioEstacionamiento(HoraInicio, HoraFin)
        self.assertEqual(x, (True, ''))

    # caso borde
    def test_Limite_Superior_HorarioValido_Apertura_Cierre(self):
        HoraInicio = datetime.time(hour = 0, minute = 0, second = 0)
        HoraFin = datetime.time(hour = 23, minute = 59, second = 59)
        x = HorarioEstacionamiento(HoraInicio, HoraFin)
        self.assertEqual(x, (True, ''))

    
    

###################################################################
# ESTACIONAMIENTO_RESERVA_FORM
###################################################################

    # malicia
    def test_EstacionamientoReserva_Vacio(self):
        form_data = {}
        form = EstacionamientoReservaForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # caso borde
    def test_EstacionamientoReserva_UnCampo(self):
        form_data = {'InicioReserva':datetime.time(6, 0)}
        form = EstacionamientoReservaForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # normal
    def test_EstacionamientoReserva_TodosCamposBien(self):
        form_data = {'InicioReserva':datetime.time(6, 0), 'FinalReserva':datetime.time(12, 0)}
        form = EstacionamientoReservaForm(data = form_data)
        self.assertEqual(form.is_valid(), True)

    # malicia
    def test_EstacionamientoReserva_InicioString(self):
        form_data = {'InicioReserva':'hola',
                                'FinalReserva':datetime.time(12, 0)}
        form = EstacionamientoReservaForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoReserva_FinString(self):
        form_data = {'InicioReserva':datetime.time(6, 0),
                                'FinalReserva':'hola'}
        form = EstacionamientoReservaForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoReserva_InicioNone(self):
        form_data = {'InicioReserva':None,
                                'FinalReserva':datetime.time(12, 0)}
        form = EstacionamientoReservaForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

    # malicia
    def test_EstacionamientoReserva_finalNone(self):
        form_data = {'InicioReserva':datetime.time(6, 0),
                                'FinalReserva':None}
        form = EstacionamientoReservaForm(data = form_data)
        self.assertEqual(form.is_valid(), False)

###################################################################
# PRUEBAS DE FUNCIONES DEL CONTROLADOR
###################################################################

##############################################################
# Estacionamiento Reserva Controlador
###################################################################

# HorarioReserva, pruebas Unitarias

    # normal
    def test_HorarioReservaInvalido_ReservacionMuyLejana(self):
        ReservaInicio = datetime.datetime(year = 2015, month = 10, day = 25,hour = 13, minute = 0, second = 0)
        ReservaFin = datetime.datetime(year = 2015, month = 10, day = 25,hour = 15, minute = 0, second = 0)
        HoraApertura = datetime.datetime(year = 2015, month = 10, day = 25,hour = 12, minute = 0, second = 0)
        HoraCierre = datetime.datetime(year = 2015, month = 10, day = 25,hour = 18, minute = 0, second = 0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'La fecha de fin de la reserva no puede ser posterior a los próximos 7 días'))

    # caso borde
    def test_HorarioReservaInvalido_InicioReservacion_Mayor_FinalReservacion(self):
        ReservaInicio = datetime.datetime(year = 2015, month = 10, day = 25,hour = 13, minute = 0, second = 0)
        ReservaFin = datetime.datetime(year = 2015, month = 10, day = 25,hour = 12, minute = 59, second = 59)
        HoraApertura = datetime.datetime(year = 2015, month = 10, day = 25,hour = 12, minute = 0, second = 0)
        HoraCierre = datetime.datetime(year = 2015, month = 10, day = 25,hour = 18, minute = 0, second = 0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'La hora de inicio de la reserva debe ser menor a la hora de fin'))

    # caso borde
    def test_HorarioReservaInvalido_TiempoTotalMenor1h(self):
        ReservaInicio = datetime.datetime(year = 2015, month = 10, day = 25,hour = 13, minute = 0, second = 0)
        ReservaFin = datetime.datetime(year = 2015, month = 10, day = 25,hour = 13, minute = 59, second = 59)
        HoraApertura = datetime.datetime(year = 2015, month = 10, day = 25,hour = 12, minute = 0, second = 0)
        HoraCierre = datetime.datetime(year = 2015, month = 10, day = 25,hour = 18, minute = 0, second = 0)
        x = validarHorarioReserva(ReservaInicio, ReservaFin, HoraApertura, HoraCierre)
        self.assertEqual(x, (False, 'El tiempo de la reserva debe ser al menos de 1 hora'))

    # malicia
    def test_Reservacion_CamposVacios(self):
        form_data = {'InicioReserva':datetime.datetime(year = 2015, month = 10, 
                                                       day = 25,hour = 6, minute = 0, 
                                                       second = 0), 
                     'FinalReserva':datetime.datetime(year = 2015, month = 10, 
                                                      day = 25,hour = 12, minute = 0,
                                                       second = 0)}
        form = EstacionamientoReservaForm(data = form_data)
        self.assertEqual(form.is_valid(), False)
 
 
 
# Objects used in some tests

esquema = Esquema(100)
esquema1 = EsquemaTarifario()
esquema1.TipoEsquema = "1"
esquema1.Tarifa = 100
esquema2 = EsquemaTarifario()
esquema2.TipoEsquema = "2"
esquema2.Tarifa = 100
esquema3 = EsquemaTarifario()
esquema3.TipoEsquema = "3"
esquema3.Tarifa = 100
esquema4 = EsquemaTarifario()
esquema4.TipoEsquema = "4"
esquema4.Tarifa = 100
esq4_difer = EsquemaDiferenciado()
esq4_difer.EsquemaTarifario = esquema4
esq4_difer.HoraPicoFin = datetime.time(18,0)
esq4_difer.HoraPicoInicio = datetime.time(15,0)
esq4_difer.TarifaPico = 200
esquema5 = EsquemaTarifario()
esquema1.TipoEsquema = "5"
esquema5.Tarifa = 100
esq5_difer = EsquemaDiferenciado()
esq5_difer.EsquemaTarifario = esquema5
esq5_difer.HoraPicoFin = None
esq5_difer.HoraPicoInicio = None
esq5_difer.TarifaPico = 200
estacionamiento = Estacionamiento()
propietario = Propietario()
propietario.NombreProp = "Pedro"
propietario.Telefono_1 = "0424-2227381"
propietario.Email_1 = "cs@cs.cs"
propietario.Rif = "V-123456785"
estacionamiento.Propietario = propietario
estacionamiento.Nombre = "Est"
estacionamiento.Direccion = "Ccs"
estacionamiento.Apertura = datetime.time(0,0)
estacionamiento.Cierre = datetime.time(23,59)
estacionamiento.NroPuesto = 10  
    
    
      
class EsquemasTarifariosTests(unittest.TestCase):
    
    
    ##  ##
    def testcostoHorasCompletasSimple(self):
        esquema = Esquema(5)
        self.assertEqual(esquema._costoHorasCompletas(4),20)
    def testcostoHorasCompletasCeroHoras(self):
        esquema = Esquema(5)
        self.assertEqual(esquema._costoHorasCompletas(0),0)
    def testcostoHorasCompletasMaximoDeHoras(self):
        esquema = Esquema(5)
        self.assertEqual(esquema._costoHorasCompletas(23),115)    
    def testcostoHorasCompletasHoraUnitaria(self):
        esquema = Esquema(5)
        self.assertEqual(esquema._costoHorasCompletas(1),5)
        
    def testcostoHorasCompletasTarifaDecimal(self): 
        esquema = Esquema(0.1)
        self.assertEqual(esquema._costoHorasCompletas(4),Decimal(0.1)*Decimal(4))
    def testcostoHorasCompletasTarifaDecimalCeroHoras(self):
        esquema = Esquema(0.1)
        self.assertEqual(esquema._costoHorasCompletas(0),0)
    def testcostoHorasCompletasTarifaDecimalMaximoDeHoras(self):
        esquema = Esquema(0.1)
        self.assertEqual(esquema._costoHorasCompletas(23),Decimal(23)*Decimal(0.1))
    def testcostoHorasCompletasTarifaDecimalHoraUnitaria(self):
        esquema = Esquema(0.1)
        self.assertEqual(esquema._costoHorasCompletas(1),Decimal(1)*Decimal(0.1))
        
    def testcostoHorasCompletasTarifaAlta(self):
        esquema = Esquema(2**30)
        self.assertEqual(esquema._costoHorasCompletas(4),4*2**30)
    def testcostoHorasCompletasTarifaAltaCeroHoras(self):
        esquema = Esquema(2**30)    
        self.assertEqual(esquema._costoHorasCompletas(0),0)
    def testcostoHorasCompletasTarifaAltaMaximoDeHoras(self):
        esquema = Esquema(2**30)   
        self.assertEqual(esquema._costoHorasCompletas(23),23*2**30)
    def testcostoHorasCompletasTarifaAltaHoraUnitaria(self):
        esquema = Esquema(2**30)
        self.assertEqual(esquema._costoHorasCompletas(1),2**30)
        
        
    ## ESQUEMA 1 ##
        
        
        
    def testcostoFraccionHoraEsquema1DecimalCeroMinutos(self):
        global esquema1
        self.assertEqual(calcularCostoReserva(esquema1,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
    def testcostoFraccionHoraEsquema1DecimalMinutoUnitario(self):
        global esquema1
        esquema1.Tarifa = 0.1
        self.assertEqual(calcularCostoReserva(esquema1,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,1)), 0.1)
    def testcostoFraccionHoraEsquema1DecimalMinutoMaximo(self):
        global esquema1
        esquema1.Tarifa = 0.1
        self.assertEqual(calcularCostoReserva(esquema1,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,59)), 0.1)
        
    def testcostoFraccionHoraEsquema1SimpleCeroMinutos(self):
        global esquema1    
        esquema1.Tarifa = 5   
        self.assertEqual(calcularCostoReserva(esquema1,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
    def testcostoFraccionHoraEsquema1SimpleMinutoUnitario(self):
        global esquema1
        esquema1.Tarifa = 5
        self.assertEqual(calcularCostoReserva(esquema1,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,1)), 5)
    def testcostoFraccionHoraEsquema1SimpleMinutoMaximo(self):
        global esquema1
        esquema1.Tarifa = 5
        self.assertEqual(calcularCostoReserva(esquema1,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,59)), 5) 
        
    def testcostoFraccionHoraEsquema1TarifaAltaCeroMinutos(self):
        global esquema1
        esquema1.Tarifa = 2**30
        self.assertEqual(calcularCostoReserva(esquema1,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
    def testcostoFraccionHoraEsquema1TarifaAltaMinutoUnitario(self):
        global esquema1
        esquema1.Tarifa = 2**30
        self.assertEqual(calcularCostoReserva(esquema1,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,1)), 2**30)
    def testcostoFraccionHoraEsquema1TarifaAltaMinutoMaximo(self):
        global esquema1
        esquema1.Tarifa = 2**30
        self.assertEqual(calcularCostoReserva(esquema1,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,59)), 2**30) 
        
        
    ## ESQUEMA 2 ##
        
        
    def testcostoFraccionHoraEsquema2DecimalCeroMinutos(self):
        global esquema2
        esquema2.Tarifa = 0.1
        self.assertEqual(calcularCostoReserva(esquema2,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
    def testcostoFraccionHoraEsquema2DecimalMinutoUnitario(self):
        global esquema2
        esquema2.Tarifa = 0.1
        self.assertEqual(calcularCostoReserva(esquema2,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,1)), Decimal(0.1)/Decimal(2))
    def testcostoFraccionHoraEsquema2DecimalMinutoMaximo(self):
        global esquema2
        esquema2.Tarifa = 0.1
        self.assertEqual(calcularCostoReserva(esquema2,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,59)), 0.1)
            
    def testcostoFraccionHoraEsquema2SimpleCeroMinutos(self):
        global esquema2
        esquema2.Tarifa = 5
        self.assertEqual(calcularCostoReserva(esquema2,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
    def testcostoFraccionHoraEsquema2SimpleMinutoUnitario(self):
        global esquema2
        esquema2.Tarifa = 5
        self.assertEqual(calcularCostoReserva(esquema2,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,1)), 2.5)
    def testcostoFraccionHoraEsquema2SimpleMinutoMaximo(self):
        global esquema2
        esquema2.Tarifa = 5
        self.assertEqual(calcularCostoReserva(esquema2,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,59)), 5) 
        
    def testcostoFraccionHoraEsquema2TarifaAltaCeroMinutos(self):
        global esquema2
        esquema2.Tarifa = 2**30
        self.assertEqual(calcularCostoReserva(esquema2,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
    def testcostoFraccionHoraEsquema2TarifaAltaMinutoUnitario(self):
        global esquema2
        esquema2.Tarifa = 2**30
        self.assertEqual(calcularCostoReserva(esquema2,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,1)), (2**30)/2)
    def testcostoFraccionHoraEsquema2TarifaAltaMaximoMinuto(self):
        global esquema2
        esquema2.Tarifa = 2**30  
        self.assertEqual(calcularCostoReserva(esquema2,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,59)), 2**30)
    
    
    ## ESQUEMA 3 ##
    
    
    def testcostoFraccionHoraEsquema3DecimalCeroMinutos(self):
        global esquema3
        esquema3.Tarifa = 0.1
        self.assertEqual(calcularCostoReserva(esquema3,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
    def testcostoFraccionHoraEsquema3DecimalMinutoUnitario(self):
        global esquema3
        esquema3.Tarifa = 0.1
        self.assertEqual(calcularCostoReserva(esquema3,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,1)), Decimal((0.1))/Decimal(60))
    def testcostoFraccionHoraEsquema3DecimalMaximoMinuto(self):
        global esquema3
        esquema3.Tarifa = 0.1
        self.assertEqual(calcularCostoReserva(esquema3,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,59)), Decimal(0.1)-Decimal((0.1))/Decimal(60))
    
    def testcostoFraccionHoraEsquema3SimpleCeroMinutos(self):
        global esquema3
        esquema3.Tarifa = 5      
        self.assertEqual(calcularCostoReserva(esquema3,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
    def testcostoFraccionHoraEsquema3SimpleMinutoUnitario(self):
        global esquema3
        esquema3.Tarifa = 5
        self.assertEqual(calcularCostoReserva(esquema3,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,1)), Decimal(5)/Decimal(60))
    def testcostoFraccionHoraEsquema3SimpleMaximoMinuto(self):
        global esquema3
        esquema3.Tarifa = 5   
        self.assertEqual(calcularCostoReserva(esquema3,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,59)), Decimal(59)*(Decimal(5)/Decimal(60))) 
        
    def testcostoFraccionHoraEsquema3TarifaAltaCeroMinutos(self):
        global esquema3
        esquema3.Tarifa = 2**30    
        self.assertEqual(calcularCostoReserva(esquema3,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
    def testcostoFraccionHoraEsquema3TarifaAltaMinutoUnitario(self):
        global esquema3
        esquema3.Tarifa = 2**30
        self.assertEqual(calcularCostoReserva(esquema3,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,1)), (Decimal(2)**Decimal(30))/Decimal(60))
    def testcostoFraccionHoraEsquema3TarifaAltaMaximoMinuto(self):
        global esquema3
        esquema3.Tarifa = 2**30
        self.assertEqual(calcularCostoReserva(esquema3,None,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,59)), Decimal('1055846126.933333333333333334'))

    ## ESQUEMA 4 ##
    
    def testcostoFraccionHoraEsquema4TarifaDecimalCeroMinutos(self):
        global esquema4
        global esq4_difer
        esquema4.Tarifa = 0.1
        self.assertEqual(calcularCostoReserva(esquema4,esq4_difer,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
        
    def testcostoFraccionHoraEsquema4SimpleCeroMinutos(self):
        global esquema4
        global esq4_difer
        esquema4.Tarifa = 100
        self.assertEqual(calcularCostoReserva(esquema4,esq4_difer,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,0)), 0)
        
    def testcostoFraccionHoraEsquema4SimpleMediaHoraRegular(self):
        global esquema4
        global esq4_difer
        esquema4.Tarifa = 100
        self.assertEqual(calcularCostoReserva(esquema4,esq4_difer,datetime.datetime(2015,1,1,0,0), datetime.datetime(2015,1,1,0,30)), Decimal(100/2))
        
    def testcostoFraccionHoraEsquema4SimpleMediaHoraPico(self):
        global esquema4
        global esq4_difer
        esquema4.Tarifa = 100
        esq4_difer.TarifaPico = 200
        self.assertEqual(calcularCostoReserva(esquema4,esq4_difer,datetime.datetime(2015,1,1,15,0), datetime.datetime(2015,1,1,15,30)), Decimal(200/2))
        
    def testcostoFraccionHoraEsquema4SimpleMinutoRegularMinutoPico(self):
        global esquema4
        global esq4_difer
        esquema4.Tarifa = 100
        esq4_difer.TarifaPico = 200
        self.assertEqual(calcularCostoReserva(esquema4,esq4_difer,datetime.datetime(2015,1,1,14,59), datetime.datetime(2015,1,1,15,1)), Decimal(200/60)+Decimal(100/60))
        
    
    ## ESQUEMA 5 ##
    
    
        
class PagarReservaTests(unittest.TestCase):
    def test_CamposVacios(self):
        form_data = {}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_NroTarjetaVacia(self):
        form_data = {'NroTarjeta': '', 'CedulaTitular': 'V12345678', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':'Mister'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_CedulaVacia(self):
        form_data = {'NroTarjeta': '12345678912345678', 'CedulaTitular': '', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':'Mister'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_NombreVacio(self):
        form_data = {'NroTarjeta': '12345678912345678', 'CedulaTitular': 'V12345678', 'NombreTitular': '', 'ProveedorCred':'Mister'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_NroTarjetaMenosDigitos(self):
        form_data = {'NroTarjeta': '1', 'CedulaTitular': 'V12345678', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':'Mister'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_NroTarjetaNegativa(self):
        form_data = {'NroTarjeta': '-1234567891234567', 'CedulaTitular': 'V12345678', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':'Mister'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_NroTarjetaMasDigitos(self):
        form_data = {'NroTarjeta': '12345678912345678', 'CedulaTitular': 'V12345678', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':'Mister'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_CedulaMasDigitos(self):
        form_data = {'NroTarjeta': '1234567891234567', 'CedulaTitular': 'V123456789', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':'Vista'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_CedulaMenosDigitos(self):
        form_data = {'NroTarjeta': '1234567891234567', 'CedulaTitular': 'V-123', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':'Vista'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), True)
    def test_CedulaSinLetra(self):
        form_data = {'NroTarjeta': '1234567891234567', 'CedulaTitular': '12345678', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':'Vista'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_CedulaOtraLetra(self):
        form_data = {'NroTarjeta': '1234567891234567', 'CedulaTitular': 'W12345678', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':'Vista'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_NombreConNumeros(self):
        form_data = {'NroTarjeta': '1234567891234567', 'CedulaTitular': 'V12345678', 'NombreTitular': 'Pedro12Pérez', 'ProveedorCred':'Vista'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_NombreConCaracteresEspeciales(self):
        form_data = {'NroTarjeta': '1234567891234567', 'CedulaTitular': 'W12345678', 'NombreTitular': 'Pedro $Pérez', 'ProveedorCred':'Vista'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_SinProveedor(self):
        form_data = {'NroTarjeta': '1234567891234567', 'CedulaTitular': 'V12345678', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':''}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_NroTarjetaConLetras(self):
        form_data = {'NroTarjeta': 'Hola, soy TeRuEl', 'CedulaTitular': 'V12345678', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':''}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_NroTarjetaConUnaLetra(self):
        form_data = {'NroTarjeta': '1234567890123456h', 'CedulaTitular': 'V12345678', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':''}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), False)
    def test_Correcto(self):
        form_data = {'NroTarjeta': '1234567891234567', 'CedulaTitular': 'V12345678', 'NombreTitular': 'Pedro Pérez', 'ProveedorCred':'Vista'}
        form = PagarReservaForm(form_data)
        self.assertEqual(form.is_valid(), True)