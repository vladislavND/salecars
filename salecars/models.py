from django.db import models


class Marks(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Models(models.Model):
    name = models.CharField(max_length=255)
    slug_name = models.CharField(max_length=255, null=True, blank=True)
    mark = models.ForeignKey(Marks, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=255)
    name_slug = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)
    name_slug = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


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
    crash = models.BooleanField(default=False)
    engine = models.CharField(max_length=255, choices=ENGINE_CHOICES)
    steering_wheel = models.CharField(max_length=255, choices=WHEEL_CHOICES)
    value = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=4)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(auto_now=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.model.name


class User(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    mobile_phone = models.CharField(max_length=12)
    price_to = models.IntegerField(null=True, blank=True)
    price_from = models.IntegerField(null=True, blank=True)
    auto = models.ManyToManyField(Auto, null=True, blank=True)
    telegram_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username


















