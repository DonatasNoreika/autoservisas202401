from django.db import models


# Create your models here.
class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=50)
    price = models.FloatField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.name} ({self.price})"


class VehicleModel(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=20)
    model = models.CharField(verbose_name="Modelis", max_length=30)

    def __str__(self):
        return f"{self.make} ({self.model})"


class Vehicle(models.Model):
    license_plate = models.CharField(verbose_name="Valstybinis numeris", max_length=10)
    vin_code = models.CharField(verbose_name="VIN kodas", max_length=17)
    client_name = models.CharField(verbose_name="Klientas", max_length=50)
    vehicle_model = models.ForeignKey(to="VehicleModel", verbose_name="Modelis", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.vehicle_model} ({self.license_plate})"


class Order(models.Model):
    date = models.DateTimeField(verbose_name="Data")
    vehicle = models.ForeignKey(to="Vehicle", verbose_name="Automobilis", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vehicle} ({self.date})"


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Užsakymas", on_delete=models.CASCADE)
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(verbose_name="Kiekis")

    def __str__(self):
        return f"{self.service.name} - {self.qty} ({self.order.date})"
