from django.contrib import admin
from .models import Service, VehicleModel, Vehicle, Order, OrderLine


class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['date', 'vehicle']
    inlines = [OrderLineInLine]


admin.site.register(Service)
admin.site.register(Vehicle)
admin.site.register(VehicleModel)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
