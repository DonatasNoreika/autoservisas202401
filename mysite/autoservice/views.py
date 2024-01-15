from django.shortcuts import render
from .models import Service, Order, Vehicle
from django.views import generic


# Create your views here.
def index(request):
    num_services = Service.objects.all().count()
    num_orders_done = Order.objects.filter(status__exact='i').count()
    num_vehicles = Vehicle.objects.all().count()
    result = {
        "num_services": num_services,
        "num_orders_done": num_orders_done,
        "num_vehicles": num_vehicles,
    }
    return render(request, template_name="index.html", context=result)


def vehicles(request):
    vehicles = Vehicle.objects.all()
    context = {
        "vehicles": vehicles,
    }
    return render(request, template_name="vehicles.html", context=context)


def vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    context = {
        "vehicle": vehicle,
    }
    return render(request, template_name="vehicle.html", context=context)


class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'
