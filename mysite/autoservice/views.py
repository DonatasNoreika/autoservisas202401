from django.shortcuts import render
from .models import Service, Order, Vehicle
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def index(request):
    num_services = Service.objects.all().count()
    num_orders_done = Order.objects.filter(status__exact='i').count()
    num_vehicles = Vehicle.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    result = {
        "num_services": num_services,
        "num_orders_done": num_orders_done,
        "num_vehicles": num_vehicles,
        "num_visits": num_visits,
    }
    return render(request, template_name="index.html", context=result)


def vehicles(request):
    vehicles = Vehicle.objects.all()
    paginator = Paginator(vehicles, per_page=3)
    page_number = request.GET.get("page")
    paged_vehicles = paginator.get_page(page_number)
    context = {
        "vehicles": paged_vehicles,
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
    paginate_by = 3


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'

def search(request):
    query = request.GET.get('query')
    vehicles = Vehicle.objects.filter(Q(client_name__icontains=query) |
                                      Q(vehicle_model__make__icontains=query) |
                                      Q(vehicle_model__model__icontains=query) |
                                      Q(license_plate__icontains=query) |
                                      Q(vin_code__icontains=query))
    context = {
        "query": query,
        "vehicles": vehicles,
    }
    return render(request, template_name='search.html', context=context)