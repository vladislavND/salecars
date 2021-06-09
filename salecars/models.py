from django.db import models


class Marks(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.CharField(max_length=255, null=True, blank=True)


class Models(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.CharField(max_length=255, null=True, blank=True)
    model = models.ForeignKey(Marks, on_delete=models.CASCADE)


class City(models.Model):
    name = models.CharField(max_length=255)
    name_slug = models.CharField(max_length=255)


class Region(models.Model):
    name = models.CharField(max_length=255)
    name_slug = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)


class Auto(models.Model):
    GAS = 'GAS'
    BENZ = 'BENZ'
    GAS_BENZ = 'GAS_BENZ'
    DIESEL = 'DIESEL'
    ELECTRO = 'ELECTRO'
    ENGINE_CHOICES = [
        (GAS, 'Газ'),
        (BENZ, 'Бензин'),
        (DIESEL, 'Дизель'),
        (ELECTRO, 'Электро'),
        (GAS_BENZ, 'Газ-Бензин')
    ]
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    WHEEL_CHOICES = [
        (LEFT, 'Левый'),
        (RIGHT, 'Правый')
    ]
    model = models.ForeignKey(Models, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    resident = models.BooleanField()
    engine = models.CharField(max_length=255, choices=ENGINE_CHOICES)
    steering_wheel = models.CharField(max_length=255, choices=WHEEL_CHOICES)
    value = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=4)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(auto_now=True)
    description = models.CharField(max_length=255, null=True, blank=True)


class User(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    mobile_phone = models.CharField(max_length=12)
    price_to = models.IntegerField(null=True, blank=True)
    price_from = models.IntegerField(null=True, blank=True)
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, null=True, blank=True)
    telegram_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)


















