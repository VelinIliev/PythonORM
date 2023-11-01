from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models


def check_name(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError("Name can only contain letters and spaces.")


def check_phone(value):
    if not value.startswith('+359') or not len(value[4:]) == 9 or not value[4:].isdigit():
        raise ValidationError("Phone number must start with a '+359' followed by 9 digits")


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[check_name, ]
    )
    age = models.PositiveIntegerField(
        validators=[
            validators.MinValueValidator(limit_value=18, message='Age must be greater than 18')
        ]
    )
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=13,
        validators=[check_phone, ]
    )
    website_url = models.URLField()


class BaseMedia(models.Model):
    title = models.CharField(
        max_length=100
    )
    description = models.TextField()
    genre = models.CharField(
        max_length=50
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']


class Book(BaseMedia):
    author = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(
                limit_value=5,
                message='Author must be at least 5 characters long'
            )]
    )
    isbn = models.CharField(
        max_length=20,
        validators=[
            validators.MinLengthValidator(
                limit_value=6,
                message='ISBN must be at least 6 characters long'
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'


class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(
                limit_value=8,
                message='Director must be at least 8 characters long'
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Movie'
        verbose_name_plural = 'Models of type - Movie'


class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(
                limit_value=9,
                message='Artist must be at least 9 characters long'
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = 'Models of type - Music'


class Product(models.Model):
    name = models.CharField(
        max_length=100
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def calculate_tax(self):
        return self.price * Decimal(0.08)

    @staticmethod
    def calculate_shipping_cost(weight: Decimal):
        return weight * Decimal(2.00)

    def format_product_name(self):
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    class Meta:
        proxy = True

    def calculate_price_without_discount(self):
        return self.price * Decimal(1.20)

    def calculate_tax(self):
        return self.price * Decimal(0.05)

    @staticmethod
    def calculate_shipping_cost(weight: Decimal):
        return weight * Decimal(1.50)

    def format_product_name(self):
        return f'Discounted Product: {self.name}'


class RechargeEnergyMixin:
    def recharge_energy(self, amount):
        self.energy = min(self.energy + amount, 100)
        self.save()


# TODO: 71/100

class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(
        max_length=100
    )
    hero_title = models.CharField(
        max_length=100
    )
    energy = models.PositiveIntegerField()


class SpiderHero(Hero):
    def swing_from_buildings(self):
        if self.energy - 80 <= 0:
            return f'{self.name} as Spider Hero is out of web shooter fluid'
        else:
            self.energy -= 80
            self.save()
            return f'{self.name} as Spider Hero swings from buildings using web shooters'

    class Meta:
        proxy = True


class FlashHero(Hero):
    def run_at_super_speed(self):
        if self.energy - 65 <= 0:
            return f'{self.name} as Flash Hero needs to recharge the speed force'
        else:
            self.energy -= 65
            self.save()
            return f'{self.name} as Flash Hero runs at lightning speed, saving the day'

    class Meta:
        proxy = True
