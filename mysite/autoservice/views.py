from django.shortcuts import render
from .models import Service, Order, Vehicle
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation

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


class MyOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')
