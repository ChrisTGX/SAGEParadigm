# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, render_to_response
from django.shortcuts import redirect
from estacionamientos.controller import *
from estacionamientos.forms import EstacionamientoExtendedForm
from estacionamientos.forms import EstacionamientoForm, PagarReservaForm
from estacionamientos.forms import EstacionamientoReserva
from estacionamientos.models import Estacionamiento, ReservasModel
from aptdaemon.logger import GREEN

listaReserva = []


# Usamos esta vista para procesar todos los estacionamientos
def estacionamientos_all(request):
    global listaReserva
    listaReserva = []
    # Si se hace un POST a esta vista implica que se quiere agregar un nuevo
    # estacionamiento
    estacionamientos = Estacionamiento.objects.all()
    if request.method == 'POST':
            # Creamos un formulario con los datos que recibimos
            form = EstacionamientoForm(request.POST)

            # Parte de la entrega era limitar la cantidad maxima de
            # estacionamientos a 5
            if len(estacionamientos) >= 5:
                    return render(request, 'templateMensaje.html',
                                  {'color':'red', 'mensaje':'No se pueden agregar más estacionamientos'})

            # Si el formulario es valido, entonces creamos un objeto con
            # el constructor del modelo
            if form.is_valid():
                obj = Estacionamiento(
                        Propietario = form.cleaned_data['propietario'],
                        Nombre = form.cleaned_data['nombre'],
                        Direccion = form.cleaned_data['direccion'],
                        Rif = form.cleaned_data['rif'],
                        Telefono_1 = form.cleaned_data['telefono_1'],
                        Telefono_2 = form.cleaned_data['telefono_2'],
                        Telefono_3 = form.cleaned_data['telefono_3'],
                        Email_1 = form.cleaned_data['email_1'],
                        Email_2 = form.cleaned_data['email_2']
                )
                obj.save()
                # Recargamos los estacionamientos ya que acabamos de agregar
                estacionamientos = Estacionamiento.objects.all()
    # Si no es un POST es un GET, y mandamos un formulario vacio
    else:
        form = EstacionamientoForm()

    return render(request, 'base.html', {'form': form, 'estacionamientos': estacionamientos})



def estacionamiento_detail(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacion = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')

    global listaReserva
    listaReserva = []
    
    if request.method == 'GET':
        form = EstacionamientoExtendedForm(initial={'NroPuesto': estacion.NroPuesto,
                                                    'Apertura': estacion.Apertura,
                                                    'Cierre': estacion.Cierre,
                                                    'Reservas_Inicio': estacion.Reservas_Inicio,
                                                    'Reservas_Cierre': estacion.Reservas_Cierre,
                                                    'Tarifa': estacion.Tarifa,
                                                    'Esquema_tarifario:': estacion.Esquema_tarifario})
        #return render(request, 'estacionamiento.html', {'form': form, 'estacionamiento': estacion})
     
    elif request.method == 'POST':
            # Leemos el formulario
            form = EstacionamientoExtendedForm(request.POST)
            # Si el formulario
            if form.is_valid() and len(form.changed_data) > 0:
                
                if ('Apertura' in form.changed_data and 
                    'Cierre' in form.changed_data and 
                    'Reservas_Inicio' in form.changed_data and 
                    'Reservas_Cierre' in form.changed_data):
                    
                    hora_in = form.cleaned_data['Apertura']
                    hora_out = form.cleaned_data['Cierre']
                    reserva_in = form.cleaned_data['Reservas_Inicio']
                    reserva_out = form.cleaned_data['Reservas_Cierre']
                    
                    estacion.Apertura = hora_in
                    estacion.Cierre = hora_out
                    estacion.Reservas_Inicio = reserva_in
                    estacion.Reservas_Cierre = reserva_out
                    
                    m_validado = HorarioEstacionamiento(hora_in, hora_out, reserva_in, reserva_out)
                    if not m_validado[0]:
                        return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})
                
                elif ('Apertura' in form.changed_data or 
                    'Cierre' in form.changed_data or 
                    'Reservas_Inicio' in form.changed_data or 
                    'Reservas_Cierre' in form.changed_data):
                    return render(request, 'templateMensaje.html', 
                                  {'color':'red', 
                                   'mensaje': 'Deben especificarse juntos los horarios de Apertura, Cierre, Inicio y Fin de Reserva.'})

                if 'Tarifa' in form.changed_data: estacion.Tarifa = form.cleaned_data['Tarifa']
                if 'Esquema_tarifario' in form.changed_data: estacion.Esquema_tarifario = form.cleaned_data['Esquema_tarifario']
                if 'NroPuesto' in form.changed_data: estacion.NroPuesto = form.cleaned_data['NroPuesto']

                estacion.save()
                
    else:
        form = EstacionamientoExtendedForm()

    return render(request, 'estacionamiento.html', {'form': form, 'estacionamiento': estacion})


def estacionamiento_reserva(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacion = Estacionamiento.objects.get(id = _id)
    except ObjectDoesNotExist:
        return render(request, '404.html')

    global listaReserva

    # Antes de entrar en la reserva, si la lista esta vacia, agregamos los
    # valores predefinidos
    if len(listaReserva) < 1:
        Puestos = ReservasModel.objects.filter(Estacionamiento = estacion).values_list('Puesto', 'InicioReserva', 'FinalReserva')
        elem1 = (estacion.Apertura, estacion.Apertura)
        elem2 = (estacion.Cierre, estacion.Cierre)
        listaReserva = [[elem1, elem2] for _ in range(estacion.NroPuesto)]

        for obj in Puestos:
            puesto = busquedaBin(obj[1], obj[2], listaReserva[obj[0]])
            listaReserva[obj[0]] = insertarReserva(obj[1], obj[2], puesto[0], listaReserva[obj[0]])


    # Si se hace un GET renderizamos los estacionamientos con su formulario
    if request.method == 'GET':
        form = EstacionamientoReserva()
        return render(request, 'estacionamientoReserva.html', {'form': form, 'estacionamiento': estacion})

    # Si es un POST estan mandando un request
    elif request.method == 'POST':
            form = EstacionamientoReserva(request.POST)
            # Verificamos si es valido con los validadores del formulario
            if form.is_valid():
                inicio_reserva = form.cleaned_data['inicio']
                final_reserva = form.cleaned_data['final']

                # Validamos los horarios con los horario de salida y entrada
                m_validado = validarHorarioReserva(inicio_reserva, final_reserva, estacion.Reservas_Inicio, estacion.Reservas_Cierre)

                # Si no es valido devolvemos el request
                if not m_validado[0]:
                    return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})

                # Si esta en un rango valido, procedemos a buscar en la lista
                # el lugar a insertar
                sources = ReservasModel.objects.filter(Estacionamiento = estacion).values_list('InicioReserva', 'FinalReserva', 'Puesto')
                if AceptarReservacion(inicio_reserva, final_reserva, estacion.NroPuesto, sources):
                    reservar(inicio_reserva, final_reserva, listaReserva)
                    reservaFinal = ReservasModel(
                                        Estacionamiento = estacion,
                                        Puesto = encontrarPuesto(sources, inicio_reserva, final_reserva, estacion.NroPuesto),
                                        InicioReserva = inicio_reserva,
                                        FinalReserva = final_reserva,
                                        Pagada = False
                                    )
                    tarifa = float(estacion.Tarifa)
                    horas_completas,fraccion_hora = calcularEstadia(inicio_reserva, final_reserva)
                    total = costoHorasCompletas(horas_completas, tarifa)
                    if estacion.Esquema_tarifario == '1':
                        total += costoFraccionHoraEsquema1(fraccion_hora, tarifa)
                    elif estacion.Esquema_tarifario == '2':
                        total += costoFraccionHoraEsquema2(fraccion_hora, tarifa)
                    elif estacion.Esquema_tarifario == '3':
                        total += costoFraccionHoraEsquema3(fraccion_hora, tarifa)
                     
                    request.method = 'GET'
                    return pagar_reserva(request, 
                                  context = {'total':total,
                                             'reserva_object':reservaFinal})

                else:
                    return render(request, 
                                  'templateMensaje.html', 
                                  {'color':'red', 
                                   'mensaje':'No hay un puesto disponible para ese horario'})
    else:
        form = EstacionamientoReserva()

    return render(request, 
                  'estacionamientoReserva.html', 
                  {'form': form, 'estacionamiento': estacion})


context_global = {}
def pagar_reserva(request, context = None):
    global context_global
    # Si tenemos un GET -> acbamos de llegar desde estacionamiento_reserva
    if request.method == 'GET':
        context_global = context
        context['form'] = PagarReservaForm()
        context['color'] = 'green'
        context['mensaje'] = 'El monto de la reserva es: %.2f' % context['total']
        return render(request, 'pagarReserva.html', context)

    # Si tenemos un POST -> el usuario esta decidiendo que quiere pagar la reserva
    elif request.method == 'POST':
        context = context_global
        form = PagarReservaForm(request.POST)
        if form.is_valid():
            print(context)
            context['reserva_object'].Pagada = True
            context['reserva_object'].save()
            context['form'] = form
            context['color'] = 'green'
            context['mensaje'] = 'Reserva pagada satisfactoriamente. Su codigo de pago es %i' % context['reserva_object'].id
            context['reserva_object'].save()
            return render(request, 'templateMensaje.html', context)
        else:
            return render(request,
                          'pagarReserva.html',
                          {'form':form})















