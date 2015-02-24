# -*- coding: utf-8 -*-

# Archivo con funciones de control para SAGE
import datetime
from decimal import Decimal

import types

# Las Tuplas de cada puesto deben tener los horarios de inicio y de cierre para que
# pueda funcionar [(7:00,7:00), (19:00,19:00)]


# Suponiendo que cada estacionamiento tiene una estructura "matricial" lista de listas
# donde si m es una matriz, m[i,j] las i corresponden a los puestos y las j corresponden a tuplas
# con el horario inicio y fin de las reservas
# [[(horaIn,horaOut),(horaIn,horaOut)],[],....]

# 
# class StrategyExample :
# 
#     def __init__(self, func=None) :
#         self.name = "Strategy Example 0"
#         if func :
#              self.execute = types.MethodType(func, self, StrategyExample)
# 
#     def execute(self) :
#         print self.name
# 
# 
# def executeReplacement1(self) :
#         print self.name + " from execute 1"
# 
# 
# def executeReplacement2(self) :
#          print self.name + " from execute 2"
# 
# if __name__ == "__main__" :
# 
#     strat0 = StrategyExample()
#     strat1 = StrategyExample(executeReplacement1)
#     strat1.name = "Strategy Example 1"
#     strat2 = StrategyExample(executeReplacement2)
#     strat2.name = "Strategy Example 2"
# 
#     strat0.execute()
#     strat1.execute()
#     strat2.execute()

class EsquemaTarifario:
	
	def __init__(self, tipoEsquema, func):
		if tipoEsquema == 1:
			self.calcularCosto = types.MethodType(func, self, EsquemaTarifario)

	def calcularCosto(self):
		pass
	


def encontrarPuesto(sources, ini, fin, nropuestos):
	nodisp = []
	for elem in sources:
		if (ini.hour*100+ini.minute) in range(elem[0].hour*100+elem[0].minute,elem[1].hour*100+elem[1].minute+1) or (fin.hour*100+fin.minute) in range(elem[0].hour*100+elem[0].minute,elem[1].hour*100+elem[1].minute+1):
			nodisp.append(elem[2])
	for i in range(nropuestos):
		if not i in nodisp:
			return i
	return -1


def ordenar(tabla):
	def obtenerClave(item):
		return item[0],item[1]
	
	return sorted(tabla, key = obtenerClave)

def solapamientoEnRangoReserva(inicio_reserva,fin_reserva,inicio,fin):
	reserva_range = range(inicio_reserva,fin_reserva)
	solapamiento_range = range(inicio,fin)
	reserva_set = set(reserva_range)
	solapamiento_set = set(solapamiento_range)
	return bool(reserva_set.intersection(solapamiento_set))

def viabilidadReservacion(tabla, x, y):
	# Devuelve True si un solapamiento se encuentra dentro del rango de una reservacion
	# False en caso contrario
	tipo = 0
	offset = 1
	best = 0
	cnt = 0
	beststart = 0
	bestend = 0
	for i in range(0,len(tabla)):
		cnt = cnt - tabla[i][offset]
		if (cnt > best) and (tabla[i][tipo] != tabla[i+1][tipo]) :
			best = cnt
			beststart = tabla[i][tipo]
			bestend = tabla[i+1][tipo]
		elif (cnt == best) and solapamientoEnRangoReserva((x.hour*100+x.minute),(y.hour*100+y.minute),tabla[i][tipo],tabla[i+1][tipo]):
			best = cnt
			beststart = tabla[i][tipo]
			bestend = tabla[i+1][tipo]
	return best,beststart,bestend


def AceptarReservacion(x, y, capacidad, sources):
	tabla = []
	for elem in sources:
		tabla.append([elem[0].hour*100+elem[0].minute, -1])
		tabla.append([elem[1].hour*100+elem[1].minute, 1])
	tabla = ordenar(tabla)
	print(tabla)
	best,beststart,bestend = viabilidadReservacion(tabla, x, y)
	print(str(best) + " " + str(beststart) + " " + str(bestend))
	if best < capacidad: 
		return True
	elif best == capacidad:
		# Si el rango del solapamiento intersecta el de la reservacion, no se acepta esta ultima
		print(x, y)
		if solapamientoEnRangoReserva((x.hour*100+x.minute),(y.hour*100+y.minute),beststart,bestend):
			return False
		else:
			return True
	return False

def calcularEstadia(hora_entrada, hora_salida):
	hora_entrada = datetime.datetime(1,1,1,hora_entrada.hour,hora_entrada.minute)
	hora_salida = datetime.datetime(1,1,1,hora_salida.hour,hora_salida.minute)
	estadia = hora_salida - hora_entrada
	horas_completas = estadia.seconds // 3600
	fraccion_hora = int(int(estadia.seconds%3600)/60) 
	return horas_completas, fraccion_hora


def costoHorasCompletas(horas,tarifa):
	return Decimal(horas) * Decimal(tarifa)

# Esquema tarifario 1
def costoFraccionHoraEsquema1(fraccion,tarifa):
	if fraccion == 0: return 0
	return Decimal(tarifa)

# Esquema tarifario 2
def costoFraccionHoraEsquema2(fraccion,tarifa):
	if fraccion == 0: return 0
	else :
		if fraccion <= 30: return Decimal(tarifa) / Decimal(2)
		return Decimal(tarifa)

# Esquema tarifario 3
def costoFraccionHoraEsquema3(fraccion,tarifa):
	if fraccion == 0: return Decimal(0)
	return Decimal(fraccion) * (Decimal(tarifa) / Decimal(60))


def HorarioEstacionamiento(HoraInicio, HoraFin, ReservaInicio, ReservaFin):
	if HoraInicio >= HoraFin:
		return (False, 'El horario de apertura debe ser menor al horario de cierre')
	if ReservaInicio >= ReservaFin:
		return (False, 'El horario de inicio de reserva debe ser menor al horario de cierre')
	if ReservaInicio < HoraInicio:
		return (False, 'El horario de inicio de reserva debe ser mayor o igual al horario de apertura del estacionamiento')
	if ReservaInicio > HoraFin:
		return (False, 'El horario de comienzo de reserva debe ser menor al horario de cierre del estacionamiento')
	if ReservaFin < HoraInicio:
		return (False, 'El horario de apertura de estacionamiento debe ser menor al horario de finalización de reservas')
	if ReservaFin > HoraFin:
		return (False, 'El horario de cierre de estacionamiento debe ser mayor o igual al horario de finalización de reservas')
	return (True, '')


# busca un puesta en el estacionamiento
def buscar(hin, hout, estacionamiento):
	if not isinstance(estacionamiento, list):
		return (-1, -1, False)
	if len(estacionamiento) == 0:
		return (-1, -1, False)
	if not isinstance(hin, datetime.time) or not isinstance(hout, datetime.time):
		return (-1, -1, False)
	for i in range(len(estacionamiento)):
		posicion = busquedaBin(hin, hout, estacionamiento[i])
		if posicion[1] == True:
			return (i, posicion[0], posicion[1])
	return (-1, -1, False)

def binaria(valor, inicio, fin, lista):
	if inicio == fin:
		return inicio
	centro = (inicio + fin) // 2
	if lista[centro][0] > valor:
		return binaria(valor, inicio, centro, lista)
	if lista[centro][0] < valor:
		return binaria(valor, centro + 1, fin, lista)
	return centro

# Busca en una lista ordenada la posicion en la que una nueva tupla
# puede ser insertado, y ademas devuelve un booleano que dice si la
# tupla puede ser insertada, es decir que sus valores no solapen alguno
# ya existente.
# Precondición: la lista debe tener ya la mayor y menor posible tupla
def busquedaBin(hin, hout, listaTuplas):
	# ln = len(listaTuplas)
	if not isinstance(listaTuplas, list):
		return (0, False)
	if len(listaTuplas) == 0:
		return (0, True)
	if not isinstance(hin, datetime.time) or not isinstance(hout, datetime.time):
		return (0, False)
	index = binaria(hin, 0, len(listaTuplas), listaTuplas)
	if index == 0:
		index = index + 1
	if listaTuplas[index][0] >= hout and listaTuplas[index - 1][1] <= hin:
		return (index, True)
	else:
		return (index, False)

# inserta ordenadamente por hora de inicio
def insertarReserva(hin, hout, puesto, listaReserva):
	# no verifica precondicion, se supone que se hace buscar antes para ver si se puede agregar
	if not isinstance(listaReserva, list):
		return None
	if len(listaReserva) == 0:
		return listaReserva
	if not isinstance(hin, datetime.time) or not isinstance(hout, datetime.time):
		return listaReserva
	tupla = (hin, hout)
	listaReserva.insert(puesto, tupla)
	# estacionamiento[puesto].sort()
	return listaReserva

def reservar(hin, hout, estacionamiento):
	if not isinstance(estacionamiento, list):
		return 1
	if len(estacionamiento) == 0:
		return 1
	if not isinstance(hin, datetime.time) or not isinstance(hout, datetime.time):
		return 1
	puesto = buscar(hin, hout, estacionamiento)
	if puesto[2] != False:
		estacionamiento[puesto[0]] = insertarReserva(hin, hout, puesto[1], estacionamiento[puesto[0]])
		return estacionamiento
	else:
		return 1


def validarHorarioReserva(ReservaInicio, ReservaFin, HorarioApertura, HorarioCierre):

	if ReservaInicio >= ReservaFin:
		return (False, 'El horario de apertura debe ser menor al horario de cierre')
	if ReservaFin.hour - ReservaInicio.hour < 1:
		return (False, 'El tiempo de reserva debe ser al menos de 1 hora')
	if ReservaFin > HorarioCierre:
		return (False, 'El horario de inicio de reserva debe estar en un horario válido')
	if ReservaInicio < HorarioApertura:
		return (False, 'El horario de cierre de reserva debe estar en un horario válido')
	return (True, '')

