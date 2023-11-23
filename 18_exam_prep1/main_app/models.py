from django.core import validators
from django.db import models


class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(movies_count=models.Count('director_movies')) \
            .order_by('-movies_count', 'full_name')


class Director(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[validators.MinLengthValidator(limit_value=2)]
    )
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown')
    years_of_experience = models.SmallIntegerField(
        validators=[validators.MinValueValidator(limit_value=0)],
        default=0
    )
    objects = DirectorManager()

    def __str__(self):
        return self.full_name


class Actor(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[validators.MinLengthValidator(limit_value=2)]
    )
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown')
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    title = models.CharField(
        max_length=150,
        validators=[validators.MinLengthValidator(limit_value=5), ]
    )
    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)
    genre = models.CharField(
        max_length=6,
        choices=(('Action', 'Action'),
                 ('Comedy', 'Comedy'),
                 ('Drama', 'Drama'),
                 ('Other', 'Other')),
        default='Other',
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[validators.MinValueValidator(limit_value=0), validators.MaxValueValidator(limit_value=10)],
        default=0
    )
    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(to=Director, on_delete=models.CASCADE, related_name='director_movies')
    starring_actor = models.ForeignKey(to=Actor, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='starring_movies')
    actors = models.ManyToManyField(to=Actor, related_name='actor_movies')
