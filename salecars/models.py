import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from telegram_config.utils.helper import without_keys

logging.basicConfig(level=logging.INFO)


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
    marks = models.ForeignKey(Marks, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
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

    def __str__(self):
        return self.model.name


class UserAutoFilter(models.Model):
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
    model = models.ForeignKey(Models, on_delete=models.CASCADE, null=True, blank=True)
    marks = models.ForeignKey(Marks, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    resident = models.BooleanField(null=True, blank=True)
    crash = models.BooleanField(default=False, null=True, blank=True)
    engine = models.CharField(max_length=255, choices=ENGINE_CHOICES, null=True, blank=True)
    steering_wheel = models.CharField(max_length=255, choices=WHEEL_CHOICES, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
    price_to = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_from = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    date = models.DateField(auto_now=True)


class Adsense(models.Model):
    user = models.ForeignKey("Users", on_delete=models.CASCADE, related_name='user_id')
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='auto_id')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='region_id')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_id')
    published = models.BooleanField(default=False)
    view = models.IntegerField(null=True, blank=True)
    pub_date = models.DateField(auto_now=True)


class Users(models.Model):
    username = models.CharField(max_length=255)
    mobile_phone = models.CharField(max_length=12, null=True, blank=True)
    telegram_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    auto = models.ManyToManyField(Auto)
    auto_filter = models.ManyToManyField(UserAutoFilter)
    adsense = models.ManyToManyField("Adsense")

    def __str__(self):
        return self.username

    @staticmethod
    def get_or_check(telegram_id):
        try:
            user = Users.objects.get(telegram_id=telegram_id)
            return user
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def get_filters(telegram_id):
        return Users.objects.get(telegram_id=telegram_id).auto_filter.all()

    def add_filter(self, **kwargs):
        user = self.get_or_check(kwargs.get('telegram_id'))
        without = {'username', 'telegram_id', 'first_name'}
        kwargs_filter = without_keys(kwargs, without)
        if user:
            auto_filter = UserAutoFilter(**kwargs_filter)
            auto_filter.save()
            user.auto_filter.add(auto_filter)
        else:
            user = Users(
                username=kwargs.get('username'), mobile_phone=kwargs.get('mobile_phone'),
                telegram_id=kwargs.get('telegram_id'), first_name=kwargs.get('first_name')
            )
            auto_filter = UserAutoFilter(**kwargs_filter)
            auto_filter.save()
            user.auto_filter.add(auto_filter)

    def create_many_to_many(self, many_model, **kwargs):
        state_user = kwargs
        without = {'username', 'mobile_phone', 'telegram_id', 'first_name'}
        state_auto = without_keys(kwargs, without)
        auto = many_model(**state_auto)
        auto.save()
        user = self.get_or_check(state_user.get('telegram_id'))
        if user:
            adsense = Adsense(
                user=user, region=state_user.get('region'),
                auto=auto, city=state_user.get('city')
            )
            adsense.save()
            user.auto.add(auto)
            user.adsense.add(adsense)
        else:
            user = Users(
                username=state_user.get('username'), mobile_phone=state_user.get('mobile_phone'),
                telegram_id=state_user.get('telegram_id'), first_name=state_user.get('first_name')
            )
            user.save()
            user.auto.add(auto)
            adsense = Adsense(
                user=user, region=state_user.get('region'),
                auto=auto, city=state_user.get('city')
            )
            adsense.save()
            user.adsense.add(adsense)



















