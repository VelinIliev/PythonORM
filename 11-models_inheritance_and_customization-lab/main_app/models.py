import enum

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.datetime_safe import date


# Create your models here.
class Animal(models.Model):
    name = models.CharField(
        max_length=100
    )
    species = models.CharField(
        max_length=100
    )
    birth_date = models.DateField()
    sound = models.CharField(
        max_length=100
    )

    @property
    def age(self):
        today = date.today()
        birth_date = self.birth_date
        current_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return current_age


class Mammal(Animal):
    fur_color = models.CharField(
        max_length=50
    )


class Bird(Animal):
    wing_span = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )


class Reptile(Animal):
    scale_type = models.CharField(
        max_length=50
    )


class Employee(models.Model):
    first_name = models.CharField(
        max_length=50
    )
    last_name = models.CharField(
        max_length=50
    )
    phone_number = models.CharField(
        max_length=10
    )

    class Meta:
        abstract = True


class ZooDisplayAnimal(Animal):
    class Meta:
        proxy = True

    def display_info(self):
        blank = ''
        extra_info = ''
        try:
            x = Mammal.objects.filter(animal_ptr_id=self.pk).get()
            extra_info = f' Its fur color is {x.fur_color}.'
        except:
            blank = ''

        try:
            x = Bird.objects.filter(animal_ptr_id=self.pk).get()
            extra_info = f' Its wingspan is {x.wing_span} cm.'
        except:
            blank = ''

        try:
            x = Reptile.objects.filter(animal_ptr_id=self.pk).get()
            extra_info = f' Its scale type is {x.scale_type}.'
        except:
            blank = ''

        return f"Meet {self.name}! It's {self.species} and it's born {self.birth_date}. " \
               f"It makes a noise like '{self.sound}'!{extra_info}"

    def is_endangered(self):
        if self.species in ('Cross River Gorilla', 'Orangutan', 'Green Turtle'):
            return True
        else:
            return False


class ZooKeeperChoices(models.TextChoices):
    MAMMALS = ('Mammals', 'Mammals')
    BIRDS = ('Birds', 'Birds')
    REPTILES = ('Reptiles', 'Reptiles')
    OTHERS = ('Others', 'Others')


def validate_specialties(value):
    if value not in ('Mammals', 'Birds', 'Reptiles', 'Others'):
        raise ValidationError('Specialty must be a valid choice.')


class ZooKeeper(Employee):
    specialty = models.CharField(
        max_length=10,
        choices=ZooKeeperChoices.choices,
        validators=[validate_specialties, ]
    )
    managed_animals = models.ManyToManyField(
        to=Animal,
        related_name='animals'
    )

    def clean(self):
        if self.specialty not in ('Mammals', 'Birds', 'Reptiles', 'Others'):
            raise ValidationError("Specialty must be a valid choice.")


class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = ((True, 'Available'), (False, 'Not Available'))
        kwargs['default'] = True
        super().__init__(*args, **kwargs)


class Veterinarian(Employee):
    license_number = models.CharField(
        max_length=10
    )
    availability = BooleanChoiceField()

    def is_available(self):
        return self.availability
