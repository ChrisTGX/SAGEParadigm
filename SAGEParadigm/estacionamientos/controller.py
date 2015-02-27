# -*- coding: utf-8 -*-
# Archivo con funciones de control para SAGE
import math
import datetime
from decimal import Decimal


class Tarifa:
	
	def __init__(self, esquema, diferenciado):
		self.esquema = esquema
		self.diferenciado = diferenciado
		self.tarifa = Decimal(self.esquema.Tarifa)
		if esquema.TipoEsquema == "1":
			self.costoFraccionHora = self._costoFraccionHoraEsquema1
		elif esquema.TipoEsquema == "2":
			self.costoFraccionHora = self._costoFraccionHoraEsquema2
		elif esquema.TipoEsquema == "3":
			self.costoFraccionHora = self._costoFraccionHoraEsquema3
		elif esquema.TipoEsquema == "4":
			self.costoFraccionHora = self._costoFraccionHoraEsquema4Pico
			self.calcularCosto = self._calcularCostoEsquema4
			self.tarifaPico = Decimal(self.diferenciado.TarifaPico)
			self.horapico_inicio = self.diferenciado.HoraPicoInicio
			self.horapico_fin = self.diferenciado.HoraPicoFin
	
	def _calcularEstadia(self, hora_entrada, hora_salida):
		estadia = hora_salida - hora_entrada
		horas_completas = (estadia.days*24) + (estadia.seconds // 3600)
		fraccion_hora = int(int(estadia.seconds%3600)/60) 
		return horas_completas, fraccion_hora
	
	def _calcularEstadiaEsquema4(self, hora_entrada, hora_salida):
		estadia = hora_salida - hora_entrada
		mins_pico = 0
		minsini = 0
		while minsini in range((estadia).seconds // 60):
			print("IF: ",(hora_entrada + datetime.timedelta(0,minsini*60)).time(), self.horapico_inicio)
				
			if (hora_entrada + datetime.timedelta(0,minsini*60)).time() == self.horapico_inicio\
				or self.horapico_inicio < (hora_entrada + datetime.timedelta(0,minsini*60)).time() < self.horapico_fin:
				minsfin = 1
				while (hora_entrada + datetime.timedelta(0,minsini*60) + datetime.timedelta(0,minsfin*60)).time() <= self.horapico_fin\
				 and (hora_entrada + datetime.timedelta(0,minsini*60) + datetime.timedelta(0,minsfin*60)).time() <= hora_salida.time():
					print((hora_entrada + datetime.timedelta(0,minsini*60) + datetime.timedelta(0,minsfin*60)).time(),self.horapico_fin,hora_salida.time())
					mins_pico += 1
					minsfin += 1
				minsini = minsini + minsfin
			minsini += 1
			
		horas_completas = ((estadia.days*24*60) + (estadia.seconds // 60) - mins_pico) // 60
		#horas_completas = max(horas_completas, 0)
		horas_pico = mins_pico // 60
		fraccion_pico = int(mins_pico % 60)
		fraccion_hora = ((estadia.seconds // 60) - (horas_pico*60 + fraccion_pico)) % 60
		print(mins_pico, horas_completas, horas_pico, fraccion_hora, fraccion_pico)
		return horas_completas, horas_pico, fraccion_hora, fraccion_pico

	def _costoHorasCompletas(self, horas):
		return Decimal(horas) * self.tarifa
	
	def _costoHorasCompletasPico(self, horas_pico):
		return Decimal(horas_pico) * self.tarifaPico 
	
	################## Esquemas ####################
	
	# Esquema tarifario 1
	def _costoFraccionHoraEsquema1(self, fraccion):
		if fraccion == 0: return 0
		return Decimal(self.tarifa)
	
	# Esquema tarifario 2
	def _costoFraccionHoraEsquema2(self, fraccion):
		if fraccion == 0: return 0
		else :
			if fraccion <= 30: return Decimal(self.tarifa) / Decimal(2)
			return Decimal(self.tarifa)
	
	# Esquema tarifario 3
	def _costoFraccionHoraEsquema3(self, fraccion):
		if fraccion == 0: return Decimal(0)
		return Decimal(fraccion) * (Decimal(self.tarifa) / Decimal(60))
	
	# Esquema tarifario 4
	def _costoFraccionHoraEsquema4Pico(self, fraccion_pico):
		if fraccion_pico == 0: return Decimal(0)
		return Decimal(fraccion_pico) * (Decimal(self.tarifaPico) / Decimal(60))
	
	#######################################################
	
	def costoFraccionHora(self, fraccion, tarifa):
		pass
	
	def _calcularCostoEsquema4(self, inicio_reserva, final_reserva):
		horas_completas,horas_pico,fraccion_hora,fraccion_pico = self._calcularEstadiaEsquema4(inicio_reserva, final_reserva)
		print("AQUI")
		total = Decimal(self._costoHorasCompletas(horas_completas))
		total += Decimal(self._costoHorasCompletasPico(horas_pico))
		total += Decimal(self._costoFraccionHoraEsquema3(fraccion_hora))
		total += Decimal(self._costoFraccionHoraEsquema4Pico(fraccion_pico))
		return total
	
	def calcularCosto(self, inicio_reserva, final_reserva):
		horas_completas,fraccion_hora = self._calcularEstadia(inicio_reserva, final_reserva)
		total = Decimal(self._costoHorasCompletas(horas_completas))
		total += Decimal(self.costoFraccionHora(fraccion_hora))
		return total
		
	
	
def encontrarPuesto(sources, ini, fin, nropuestos):
	nodisp = []
	today = datetime.datetime.today()
	for elem in sources:
		if ((ini - today).days*10000+ini.hour*100+ini.minute) in range((elem[0] - today.date()).days*10000+elem[1].hour*100+elem[1].minute,
											(elem[2] - today.date()).days*10000+elem[3].hour*100+elem[3].minute+1)\
											or\
			((fin - today).days*10000+fin.hour*100+fin.minute) in range((elem[0] - today.date()).days*10000+elem[1].hour*100+elem[1].minute,
																	(elem[2] - today.date()).days*10000+elem[3].hour*100+elem[3].minute+1):
			nodisp.append(elem[4])
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


def viabilidadReservacion(tabla, inicio, final):
	# Devuelve True si un solapamiento se encuentra dentro del rango de una reservacion
	# False en caso contrario
	tipo = 0
	offset = 1
	best = 0
	cnt = 0
	beststart = 0
	bestend = 0
	today = datetime.datetime.today()
	for i in range(0,len(tabla)):
		cnt = cnt - tabla[i][offset]
		if (cnt > best) and (tabla[i][tipo] != tabla[i+1][tipo]) :
			best = cnt
			beststart = tabla[i][tipo]
			bestend = tabla[i+1][tipo]
		elif (cnt == best) and solapamientoEnRangoReserva(((inicio - today).days*10000+inicio.hour*100+inicio.minute),((final - today).days*10000+final.hour*100+final.minute),tabla[i][tipo],tabla[i+1][tipo]):
			best = cnt
			beststart = tabla[i][tipo]
			bestend = tabla[i+1][tipo]
	return best,beststart,bestend


def AceptarReservacion(inicio, final, capacidad, sources):
	tabla = []
	today = datetime.datetime.today()
	for elem in sources:
		diasIni = (elem[0] - today.date()).days
		diasFin = (elem[2] - today.date()).days
		tabla.append([diasIni*10000 + elem[1].hour*100 + elem[1].minute, -1])
		tabla.append([diasFin*10000 + elem[3].hour*100 + elem[3].minute, 1])

	tabla = ordenar(tabla)
	
	best,beststart,bestend = viabilidadReservacion(tabla, inicio, final)
	
	if best < capacidad: 
		return True
	elif best == capacidad:
		# Si el rango del solapamiento intersecta el de la reservacion, no se acepta esta ultima
		if solapamientoEnRangoReserva(((inicio.date() - today.date()).days*10000+inicio.hour*100+inicio.minute),((final.date() - today.date()).days*10000+final.hour*100+final.minute),beststart,bestend):
			return False
		else:
			return True
	return False


def HorarioEstacionamiento(HoraInicio, HoraFin):
	if HoraInicio >= HoraFin:
		return (False, 'El horario de apertura debe ser menor al horario de cierre')
	return (True, '')


def validarHorarioReserva(ReservaInicio, ReservaFin, HorarioApertura, HorarioCierre):
	today = datetime.datetime.today()
	nextweek = today + datetime.timedelta(7)
	
	if ReservaInicio >= ReservaFin:
		return (False, 'La hora de inicio de la reserva debe ser menor a la hora de fin')
	if ReservaFin - ReservaInicio < datetime.timedelta(0, 3600):
		return (False, 'El tiempo de la reserva debe ser al menos de 1 hora')
	if ReservaInicio.date() < today.date():
		return (False, 'La fecha de inicio de la reserva no puede ser anterior al día actual')
	if ReservaFin.date() > nextweek.date():
		return (False, 'La fecha de fin de la reserva no puede ser posterior a los próximos 7 días')
	if ReservaFin.time() > HorarioCierre:
		return (False, 'El horario de fin de la reserva debe estar en un horario válido')
	if ReservaInicio.time() < HorarioApertura:
		return (False, 'El horario de inicio de la reserva debe estar en un horario válido')
	
	if HorarioApertura <= HorarioCierre: dia = 1
	else: dia = 2
	hora1 = datetime.datetime(1,1,1,HorarioApertura.hour,HorarioApertura.minute)
	hora2 = datetime.datetime(1,1,dia,HorarioCierre.hour,HorarioCierre.minute) + datetime.timedelta(0,60)
	tiempoFuncionamiento = (hora2 - hora1)
	if tiempoFuncionamiento.days == 1 and tiempoFuncionamiento.seconds == 0: # Funciona las 24 horas
		if ReservaFin - ReservaInicio > datetime.timedelta(7):
			return (False, 'El tiempo de la reserva en un estacionamiento abierto las 24 horas debe ser a lo sumo de 7 días')
	else:
		if ReservaFin.date() != ReservaInicio.date():
			return (False, 'El tiempo de la reserva está fuera del horario de funcionamiento del estacionamiento')
	
	return (True, '')
