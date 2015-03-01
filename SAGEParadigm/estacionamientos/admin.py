# -*- coding: utf-8 -*-
from django.contrib import admin
from estacionamientos.models import Estacionamiento, Reserva, Pago,\
    EsquemaTarifario, EsquemaDiferenciado, Propietario

admin.site.register(Estacionamiento)

class PagoAdmin(admin.ModelAdmin):
    list_display = ['ID_Pago', 'NroTarjeta', 'NombreTitular', 'Monto']

admin.site.register(Pago, PagoAdmin)

class ReservaAdmin(admin.ModelAdmin):
    list_display = ['Puesto', 'Estacionamiento', 'FechaInicio', 'HoraInicio', 'FechaFinal', 'HoraFinal']

admin.site.register(Reserva, ReservaAdmin)

admin.site.register(EsquemaTarifario)
admin.site.register(EsquemaDiferenciado)
admin.site.register(Propietario)