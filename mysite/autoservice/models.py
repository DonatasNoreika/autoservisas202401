from django.db import models


# Create your models here.
class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=50)
    price = models.FloatField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.name} ({self.price})"

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class VehicleModel(models.Model):
    make = models.CharField(verbose_name="Gamintojas", max_length=20)
    model = models.CharField(verbose_name="Modelis", max_length=30)

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = 'Automobilio modelis'
        verbose_name_plural = 'Automobilio modeliai'


class Vehicle(models.Model):
    license_plate = models.CharField(verbose_name="Valstybinis numeris", max_length=10)
    vin_code = models.CharField(verbose_name="VIN kodas", max_length=17)
    client_name = models.CharField(verbose_name="Klientas", max_length=50)
    vehicle_model = models.ForeignKey(to="VehicleModel", verbose_name="Modelis", on_delete=models.SET_NULL, null=True)
    photo = models.ImageField('Nuotrauka', upload_to='vehicles', null=True, blank=True)

    def __str__(self):
        return f"{self.vehicle_model} ({self.license_plate})"

    class Meta:
        verbose_name = 'Automobilis'
        verbose_name_plural = 'Automobiliai'


class Order(models.Model):
    date = models.DateTimeField(verbose_name="Data")
    vehicle = models.ForeignKey(to="Vehicle", verbose_name="Automobilis", on_delete=models.CASCADE)

    STATUS = (
        ('p', "Patvirtinta"),
        ('v', "Vykdoma"),
        ('i', "Įvykdyta"),
        ('a', "Atšaukta"),
    )

    status = models.CharField(verbose_name="Būsena", max_length=1, choices=STATUS, default="p")

    def total(self):
        total = 0
        for line in self.lines.all():
            total += line.line_sum()
        return total

    def __str__(self):
        return f"{self.vehicle} ({self.date}) - {self.total()}"

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(verbose_name="Kiekis")

    def line_sum(self):
        return self.service.price * self.qty

    def __str__(self):
        return f"{self.service} - {self.qty} - {self.line_sum()}"

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'
