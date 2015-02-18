# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.shortcuts import redirect
from estacionamientos.controller import *
from estacionamientos.forms import EstacionamientoExtendedForm
from estacionamientos.forms import EstacionamientoForm, PagarReservaForm
from estacionamientos.forms import EstacionamientoReserva
from estacionamientos.models import Estacionamiento, ReservasModel

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

    if request.method == 'POST':
            # Leemos el formulario
            form = EstacionamientoExtendedForm(request.POST)
            # Si el formulario
            if form.is_valid() and len(form.changed_data) > 1:
                
                if ('horarioin' in form.changed_data and 
                    'horarioout' in form.changed_data and 
                    'horario_reserin' in form.changed_data and 
                    'horario_reserout' in form.changed_data):
                    
                    hora_in = form.cleaned_data['horarioin']
                    hora_out = form.cleaned_data['horarioout']
                    reserva_in = form.cleaned_data['horario_reserin']
                    reserva_out = form.cleaned_data['horario_reserout']
                    
                    estacion.Apertura = hora_in
                    estacion.Cierre = hora_out
                    estacion.Reservas_Inicio = reserva_in
                    estacion.Reservas_Cierre = reserva_out
                    
                    m_validado = HorarioEstacionamiento(hora_in, hora_out, reserva_in, reserva_out)
                    if not m_validado[0]:
                        return render(request, 'templateMensaje.html', {'color':'red', 'mensaje': m_validado[1]})
                
                else:
                    return render(request, 'templateMensaje.html', 
                                  {'color':'red', 
                                   'mensaje': 'Deben especificarse juntos los horarios de Apertura, Cierre, Inicio y Fin de Reserva.'})

                if 'tarifa' in form.changed_data: estacion.Tarifa = form.cleaned_data['tarifa']
                if 'esquema_tarifario' in form.changed_data: estacion.Esquema_tarifario = form.cleaned_data['esquema_tarifario']
                if 'puestos' in form.changed_data: estacion.NroPuesto = form.cleaned_data['puestos']

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
                x = buscar(inicio_reserva, final_reserva, listaReserva)
                if x[2] == True :
                    reservar(inicio_reserva, final_reserva, listaReserva)
                    reservaFinal = ReservasModel(
                                        Estacionamiento = estacion,
                                        Puesto = x[0],
                                        InicioReserva = inicio_reserva,
                                        FinalReserva = final_reserva,
                                        Pagada = False
                                    )
                    reservaFinal.save()
                    tarifa = float(estacion.Tarifa)
                    horas_completas,fraccion_hora = calcularEstadia(inicio_reserva, final_reserva)
                    total = costoHorasCompletas(horas_completas, tarifa)
                    if estacion.Esquema_tarifario == '1':
                        total += costoFraccionHoraEsquema1(fraccion_hora, tarifa)
                    elif estacion.Esquema_tarifario == '2':
                        total += costoFraccionHoraEsquema2(fraccion_hora, tarifa)
                    elif estacion.Esquema_tarifario == '3':
                        total += costoFraccionHoraEsquema3(fraccion_hora, tarifa)
                        
                    return redirect('pagarReserva', 
                                    context = {'total':total,
                                               'reserva_object':reservaFinal
                                               }
                    )
                
                else:
                    return render(request, 
                                  'templateMensaje.html', 
                                  {'color':'red', 
                                   'mensaje':'No hay un puesto disponible para ese horario'
                                  }
                    )
    else:
        form = EstacionamientoReserva()

    return render(request, 
                  'estacionamientoReserva.html', 
                  {'form': form, 'estacionamiento': estacion})



def pagarReserva(request, context):
    # Si tenemos un GET -> acbamos de llegar desde estacionamiento_reserva
    if request.method == 'GET':
        return render('pagarReserva.html',
                      {'color':'green', 
                       'mensaje':'Se realizó la reserva exitosamente. El monto de la reserva es: %.2f' % context['total'],
                       'monto_decimal':total
                       }
        )
    # Si tenemos un POST -> el usuario esta decidiendo si quiere o no pagar la reserva
    elif request.method == 'POST':
        form = PagarReservaForm(request.POST)
        if form.is_valid():
            context['reserva_object'].Pagada = True
            return render('templateMensaje.html',
                          {'color':'green',
                           'mensaje':'Reserva pagada satisfactoriamente. Su codigo de pago es %i' % context['reserva_object'].primary_key
                          }
            )
        else:
            return redirect('estacionamientos_all')


