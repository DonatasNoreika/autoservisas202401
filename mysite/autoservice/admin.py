from django.contrib import admin
from .models import Service, VehicleModel, Vehicle, Order, OrderLine


class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['date', 'vehicle']
    inlines = [OrderLineInLine]


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'vehicle_model', 'license_plate', 'vin_code']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


admin.site.register(Service, ServiceAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleModel)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
