from django.shortcuts import render
from .models import Service, Order, Vehicle


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
