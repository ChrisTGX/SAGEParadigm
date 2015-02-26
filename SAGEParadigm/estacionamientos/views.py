# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import redirect
from estacionamientos.controller import *
from estacionamientos.forms import EstacionamientoExtendedForm
from estacionamientos.forms import EstacionamientoForm, PagarReservaForm
from estacionamientos.forms import EstacionamientoReserva
from estacionamientos.forms import EsquemaTarifarioForm, EsquemaDiferenciadoForm
from estacionamientos.models import Estacionamiento, Reserva, Pago, EsquemaTarifario, EsquemaDiferenciado


listaReserva = []
context_global = {}


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
                        Propietario = form.cleaned_data['Propietario'],
                        Nombre = form.cleaned_data['Nombre'],
                        Direccion = form.cleaned_data['Direccion'],
                        Rif = form.cleaned_data['Rif'],
                        Telefono_1 = form.cleaned_data['Telefono_1'],
                        Telefono_2 = form.cleaned_data['Telefono_2'],
                        Telefono_3 = form.cleaned_data['Telefono_3'],
                        Email_1 = form.cleaned_data['Email_1'],
                        Email_2 = form.cleaned_data['Email_2']
                )
                obj.save()
                
                objEsquem = EsquemaTarifario(
                        Estacionamiento = obj
                )
                objEsquem.save()
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
        esquema = EsquemaTarifario.objects.get(Estacionamiento = estacion)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    
    diferenciado = None
    
    global listaReserva
    listaReserva = []
    
    if request.method == 'GET':
        fields_initialParam = {'NroPuesto': estacion.NroPuesto}
        if estacion.Apertura: fields_initialParam['Apertura'] = estacion.Apertura.strftime('%H:%M')
        if estacion.Cierre: fields_initialParam['Cierre'] = estacion.Cierre.strftime('%H:%M')
        if estacion.Reservas_Inicio: fields_initialParam['Reservas_Inicio'] = estacion.Reservas_Inicio.strftime('%H:%M')
        if estacion.Reservas_Cierre: fields_initialParam['Reservas_Cierre'] = estacion.Reservas_Cierre.strftime('%H:%M')
       
        formParam = EstacionamientoExtendedForm(initial = fields_initialParam)

        formEsquem = EsquemaTarifarioForm(instance = esquema)
        
        if esquema.TipoEsquema == "4":
            diferenciado = EsquemaDiferenciado.objects.get(EsquemaTarifario = esquema)
            
            fields_initialDifer = {'TarifaPico': diferenciado.TarifaPico}
            if diferenciado.HoraPicoInicio: fields_initialDifer['HoraPicoInicio'] = diferenciado.HoraPicoInicio.strftime('%H:%M')
            if diferenciado.HoraPicoFin: fields_initialDifer['HoraPicoFin'] = diferenciado.HoraPicoFin.strftime('%H:%M')
            
            formDifer = EsquemaDiferenciadoForm(initial = fields_initialDifer)
        else:
            diferenciado = None
            formDifer = None
        
    elif request.method == 'POST':
        # Leemos el formulario
        formParam = EstacionamientoExtendedForm(request.POST)
        formEsquem = EsquemaTarifarioForm(request.POST)
        if esquema.TipoEsquema == "4":
            diferenciado = EsquemaDiferenciado.objects.get(EsquemaTarifario = esquema)
            formDifer = EsquemaDiferenciadoForm(request.POST)
        else:
            diferenciado = None
            formDifer = None
            
        # Si el formulario
        if formParam.is_valid() and formEsquem.is_valid() and (len(formParam.changed_data) > 0 or len(formEsquem.changed_data) > 0):
            if not formDifer or formDifer.is_valid():
                if ('Apertura' in formParam.changed_data and 
                    'Cierre' in formParam.changed_data and 
                    'Reservas_Inicio' in formParam.changed_data and 
                    'Reservas_Cierre' in formParam.changed_data):
                    
                    hora_in = formParam.cleaned_data['Apertura']
                    hora_out = formParam.cleaned_data['Cierre']
                    reserva_in = formParam.cleaned_data['Reservas_Inicio']
                    reserva_out = formParam.cleaned_data['Reservas_Cierre']
                    
                    estacion.Apertura = hora_in
                    estacion.Cierre = hora_out
                    estacion.Reservas_Inicio = reserva_in
                    estacion.Reservas_Cierre = reserva_out
                    
                    m_validado = HorarioEstacionamiento(hora_in, hora_out, reserva_in, reserva_out)
                    if not m_validado[0]:
                        return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})
                
                elif ('Apertura' in formParam.changed_data or 
                    'Cierre' in formParam.changed_data or 
                    'Reservas_Inicio' in formParam.changed_data or 
                    'Reservas_Cierre' in formParam.changed_data):
                    return render(request, 'templateMensaje.html', 
                                  {'color':'red', 
                                   'mensaje': 'Deben especificarse juntos los horarios de Apertura, Cierre, Inicio y Fin de Reserva.'})
                
                if 'NroPuesto' in formParam.changed_data: estacion.NroPuesto = formParam.cleaned_data['NroPuesto']
                                
                estacion.save()
                
                estacion = Estacionamiento.objects.get(id = _id)

                esquema.TipoEsquema = formEsquem.cleaned_data['TipoEsquema']  
                esquema.Tarifa = formEsquem.cleaned_data['Tarifa']
                               
                esquema.save()
                
                if formEsquem.cleaned_data['TipoEsquema'] == "4":
                    esquema = EsquemaTarifario.objects.get(Estacionamiento = estacion)
                    
                    if diferenciado:
                        diferenciado.HoraPicoInicio = formDifer.cleaned_data['HoraPicoInicio']
                        diferenciado.HoraPicoFin = formDifer.cleaned_data['HoraPicoFin']
                        diferenciado.TarifaPico = formDifer.cleaned_data['TarifaPico']
                    else:
                        diferenciado = EsquemaDiferenciado(
                                        EsquemaTarifario = esquema
                                        )
                    diferenciado.save()
                    
                    diferenciado = EsquemaDiferenciado.objects.get(EsquemaTarifario = esquema)
                    formDifer = EsquemaDiferenciadoForm(instance = diferenciado)
                    
                else:
                    if diferenciado: diferenciado.delete()
                    formDifer = None
                        
    else:
        formParam = EstacionamientoExtendedForm()
        formEsquem = EsquemaTarifarioForm()
        formDifer = EsquemaDiferenciadoForm()
        
    return render(request, 'estacionamiento.html', 
                  {'formParam': formParam, 'formEsquem': formEsquem, 'formDifer': formDifer, 
                   'estacionamiento': estacion, 'esquema': esquema, 'diferenciado': diferenciado})




def estacionamiento_reserva(request, _id):
    _id = int(_id)
    # Verificamos que el objeto exista antes de continuar
    try:
        estacion = Estacionamiento.objects.get(id = _id)
        esquema = EsquemaTarifario.objects.get(Estacionamiento = estacion)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    
    if esquema.TipoEsquema == "4":
        diferenciado = EsquemaDiferenciado.objects.get(EsquemaTarifario = esquema)
    else:
        diferenciado = None
    
    global listaReserva

    # Antes de entrar en la reserva, si la lista esta vacia, agregamos los
    # valores predefinidos
    if len(listaReserva) < 1:
        Puestos = Reserva.objects.filter(Estacionamiento = estacion).values_list('Puesto', 'FechaInicio', 'HoraInicio', 'FechaFinal', 'HoraFinal')
        elem1 = (estacion.Apertura, estacion.Apertura)
        elem2 = (estacion.Cierre, estacion.Cierre)
        listaReserva = [[elem1, elem2] for _ in range(estacion.NroPuesto)]

        for obj in Puestos:
            puesto = busquedaBin(obj[1], obj[2], listaReserva[obj[0]])
            listaReserva[obj[0]] = insertarReserva(obj[1], obj[2], puesto[0], listaReserva[obj[0]])


    # Si se hace un GET renderizamos los estacionamientos con su formulario
    if request.method == 'GET':
        form = EstacionamientoReserva()
        return render(request, 
                      'estacionamientoReserva.html',
                      {'form': form, 
                       'estacionamiento': estacion, 'esquema': esquema, 'diferenciado': diferenciado})

    # Si es un POST estan mandando un request
    elif request.method == 'POST':
        form = EstacionamientoReserva(request.POST)
        # Verificamos si es valido con los validadores del formulario
        if form.is_valid():
            # Inicio Reserva
            year = form.cleaned_data['FechaInicio'].year
            month = form.cleaned_data['FechaInicio'].month
            day = form.cleaned_data['FechaInicio'].day
            hour = form.cleaned_data['HoraInicio'].hour
            minute = form.cleaned_data['HoraInicio'].minute
            
            inicio_reserva = datetime.datetime(year, month, day, hour, minute)
            
            # Fin Reserva
            year = form.cleaned_data['FechaFinal'].year
            month = form.cleaned_data['FechaFinal'].month
            day = form.cleaned_data['FechaFinal'].day
            hour = form.cleaned_data['HoraFinal'].hour
            minute = form.cleaned_data['HoraFinal'].minute
            
            final_reserva = datetime.datetime(year, month, day, hour, minute)
            
            # Validamos los horarios con los horario de salida y entrada
            m_validado = validarHorarioReserva(inicio_reserva, final_reserva, estacion.Reservas_Inicio, estacion.Reservas_Cierre)

            # Si no es valido devolvemos el request
            if not m_validado[0]:
                return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})

            # Si esta en un rango valido, procedemos a buscar en la lista
            # el lugar a insertar
            sources = Reserva.objects.filter(Estacionamiento = estacion).values_list('FechaInicio', 'HoraInicio','FechaFinal', 'HoraFinal','Puesto')
            
            if AceptarReservacion(inicio_reserva, final_reserva, estacion.NroPuesto, sources):
                reservar(inicio_reserva, final_reserva, listaReserva)
                reservaFinal = Reserva(
                                    Estacionamiento = estacion,
                                    Puesto = encontrarPuesto(sources, inicio_reserva, final_reserva, estacion.NroPuesto),
                                    FechaInicio = datetime.date(inicio_reserva.year, inicio_reserva.month, inicio_reserva.day),
                                    HoraInicio = datetime.time(inicio_reserva.hour, inicio_reserva.minute),
                                    FechaFinal = datetime.date(final_reserva.year, final_reserva.month, final_reserva.day),
                                    HoraFinal = datetime.time(final_reserva.hour, final_reserva.minute),
                                    Pagada = False
                                )

                esquemaTar = Tarifa(esquema, diferenciado)
                total = esquemaTar.calcularCosto(inicio_reserva, final_reserva)
                 
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
                  {'form': form, 
                   'estacionamiento': estacion, 'esquema': esquema, 'diferenciado': diferenciado})



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
            context['reserva_object'].Pagada = True
            context['reserva_object'].save()
            context['form'] = form
            
            obj = Pago(
                    ID_Pago = context['reserva_object'],
                    NroTarjeta = form.cleaned_data['NroTarjeta'],
                    ProveedorCred = form.cleaned_data['ProveedorCred'],
                    CedulaTitular = form.cleaned_data['CedulaTitular'],
                    NombreTitular = form.cleaned_data['NombreTitular'],
                    Monto = context['total']
            )
            obj.save()
            
            context['color'] = 'green'
            context['mensaje'] = 'Reserva pagada satisfactoriamente. Su codigo de pago es %i' % context['reserva_object'].id
            context['reserva_object'].save()
            return render(request, 'templateMensaje.html', context)
        else:
            return render(request,
                          'pagarReserva.html',
                          {'form':form})















