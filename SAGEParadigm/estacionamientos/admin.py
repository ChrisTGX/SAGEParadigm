# -*- coding: utf-8 -*-
from django.contrib import admin
from estacionamientos.models import Estacionamiento, Reserva, Pago,\
    EsquemaTarifario, EsquemaDiferenciado

admin.site.register(Estacionamiento)
admin.site.register(Reserva)

class PagoAdmin(admin.ModelAdmin):
    list_display = ['ID_Pago', 'NroTarjeta', 'NombreTitular', 'Monto']

admin.site.register(Pago, PagoAdmin)
admin.site.register(EsquemaTarifario)
admin.site.register(EsquemaDiferenciado)