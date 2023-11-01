from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core import validators
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            validators.MinLengthValidator(
                limit_value=2,
                message="Name must be at least 2 characters long."),
            validators.MaxLengthValidator(
                limit_value=100,
                message="Name cannot exceed 100 characters."),
        ]
    )
    location = models.CharField(
        max_length=200,
        validators=[
            validators.MinLengthValidator(
                limit_value=2,
                message="Location must be at least 2 characters long."),
            validators.MaxLengthValidator(
                limit_value=200,
                message="Location cannot exceed 200 characters."),
        ]
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(
                limit_value=Decimal('0.00'),
                message="Rating must be at least 0.00."),
            validators.MaxValueValidator(
                limit_value=Decimal('5.00'),
                message="Rating cannot exceed 5.00."),
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"


def validate_menu_categories(value):
    categories = ("Appetizers", "Main Course", "Desserts")
    for category in categories:
        if category not in value:
            raise ValidationError(
                'The menu must include each of the categories "Appetizers", "Main Course", "Desserts".'
            )


class Menu(models.Model):
    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        validators=[validate_menu_categories, ]
    )
    restaurant = models.ForeignKey(
        to='Restaurant',
        on_delete=models.CASCADE
    )


class ReviewMixin(models.Model):
    reviewer_name = models.CharField(
        max_length=100
    )
    rating = models.PositiveIntegerField(validators=[validators.MaxValueValidator(
        limit_value=5,
        message=f'Rating cannot exceed 5.'
    )])
    review_content = models.TextField()

    class Meta:
        abstract = True
        ordering = ['-rating']


class RestaurantReview(ReviewMixin):
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True
        ordering = ['-rating']
        verbose_name = "Restaurant Review"
        verbose_name_plural = "Restaurant Reviews"
        unique_together = ('reviewer_name', 'restaurant')


class RegularRestaurantReview(RestaurantReview):
    ...


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(
        max_length=100
    )

    class Meta:
        ordering = ['-rating']
        verbose_name = "Food Critic Review"
        verbose_name_plural = "Food Critic Reviews"
        unique_together = ('reviewer_name', 'restaurant')


class MenuReview(ReviewMixin):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-rating']
        verbose_name = "Menu Review"
        verbose_name_plural = "Menu Reviews"
        unique_together = ('reviewer_name', 'menu')
        indexes = [
            models.Index(fields=['menu'], name='main_app_menu_review_menu_id'),
        ]

    def __str__(self):
        return f"{self.reviewer_name}'s Review for {self.menu.name}"
