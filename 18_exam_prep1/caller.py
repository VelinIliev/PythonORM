import os
from decimal import Decimal

import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie


# from django.utils.crypto import get_random_string
# from django.utils import timezone
# from faker import Faker
# import random


# def create_data():
#     fake = Faker()
#
#     def random_birth_date():
#         return fake.date_of_birth(minimum_age=18, maximum_age=80)
#
#     def random_nationality():
#         return fake.country()
#
#     def random_boolean():
#         return random.choice([True, False])
#
#     for _ in range(10):
#         Director.objects.create(
#             full_name=fake.name(),
#             birth_date=random_birth_date(),
#             nationality=random_nationality(),
#             years_of_experience=random.randint(0, 30)
#         )
#
#     for _ in range(10):
#         Actor.objects.create(
#             full_name=fake.name(),
#             birth_date=random_birth_date(),
#             nationality=random_nationality(),
#             is_awarded=random_boolean()
#         )
#
#     for _ in range(10):
#         director = random.choice(Director.objects.all())
#         starring_actor = random.choice(Actor.objects.all())
#         actors = list(Actor.objects.exclude(id=starring_actor.id))
#         actors = random.sample(actors, min(5, len(actors)))
#
#         Movie.objects.create(
#             title=fake.text(30).split('.')[0],
#             release_date=fake.date_this_century(),
#             storyline=fake.text(),
#             genre=random.choice(['Action', 'Comedy', 'Drama', 'Other']),
#             rating=round(random.uniform(0, 10), 1),
#             is_classic=random_boolean(),
#             is_awarded=random_boolean(),
#             director=director,
#             starring_actor=starring_actor
#         ).actors.set(actors)


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    if search_name is not None and search_nationality is not None:
        directors = Director.objects.filter(Q(full_name__icontains=search_name) &
                                            Q(nationality__icontains=search_nationality))
    elif search_name is not None:
        directors = Director.objects.filter(full_name__icontains=search_name)
    else:
        directors = Director.objects.filter(nationality__icontains=search_nationality)

    directors = directors.order_by('full_name')

    if not directors:
        return ''

    return '\n'.join(
        f'Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}' for d in
        directors)


def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()
    if not director:
        return ''
    return f'Top Director: {director.full_name}, movies: {director.movies_count}.'


def get_top_actor():
    actor = Actor.objects.prefetch_related('starring_movies') \
        .annotate(
        num_of_movies=Count('starring_movies'),
        movies_avg_rating=Avg('starring_movies__rating')) \
        .order_by('-num_of_movies', 'full_name') \
        .first()
    if not actor or not actor.num_of_movies:
        return ""
    movies = ", ".join(movie.title for movie in actor.starring_movies.all() if movie)
    return f"Top Actor: {actor.full_name}, starring in movies: {movies}, movies average rating: {actor.movies_avg_rating:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(num_of_movies=Count('actor_movies')) \
                 .order_by('-num_of_movies', 'full_name')[:3]

    if not actors or not actors[0].num_of_movies:
        return ""

    return '\n'.join(f'{a.full_name}, participated in {a.num_of_movies} movies' for a in actors)


def get_top_rated_awarded_movie():
    movie = Movie.objects.filter(is_awarded=True).order_by('-rating', 'title').first()

    if movie is None:
        return ''

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else 'N/A'
    actors = ', '.join(a.full_name for a in movie.actors.order_by('full_name'))

    return f'Top rated awarded movie: {movie.title}, rating: {movie.rating:.1f}. Starring actor: {starring_actor}. ' \
           f'Cast: {actors}.'


def increase_rating():
    movies = Movie.objects.filter(is_classic=True, rating__lte=9.9)

    if not movies:
        return 'No ratings increased.'

    for movie in movies:
        movie.rating = movie.rating + Decimal(0.1)
        movie.save()

    return f'Rating increased for {len(movies)} movies.'

# create_data()
# directors = Director.objects.get_directors_by_movies_count()
# for director in directors:
#     print(f"{director.full_name} - Movies Count: {director.movies_count}")
# print(get_directors(search_name='Geo', search_nationality='ho'))
# print(get_top_director())
# print(get_top_actor())
# print(get_actors_by_movies_count())

# print(get_top_rated_awarded_movie())
# print(increase_rating())
