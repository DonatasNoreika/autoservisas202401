from django.contrib import admin
from .models import Service, VehicleModel, Vehicle, Order, OrderLine


class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ['qty', 'service']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['date', 'vehicle', 'client', 'deadline', 'status']
    list_editable = ["client", 'deadline', 'status']
    inlines = [OrderLineInLine]


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'vehicle_model', 'license_plate', 'vin_code']
    list_filter = ['client_name', 'vehicle_model']
    search_fields = ['license_plate', 'vin_code']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


admin.site.register(Service, ServiceAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleModel)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
