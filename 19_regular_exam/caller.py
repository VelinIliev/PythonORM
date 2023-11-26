import os
import random

import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review


# Create and run your queries within functions

# from faker import Faker


# def create_entreies():
#     fake = Faker()
#
#     # Create 10 random authors
#     authors = []
#     for _ in range(10):
#         author = Author.objects.create(
#             full_name=fake.name(),
#             email=fake.email(),
#             birth_year=random.randint(1900, 2005),
#             website=fake.url(),
#         )
#         authors.append(author)
#
#     # Create 10 random articles and associate them with random authors
#     for _ in range(10):
#         article = Article.objects.create(
#             title=fake.sentence(),
#             content=fake.paragraph(),
#             category=random.choice(['Technology', 'Science', 'Education']),
#         )
#
#         # Choose a random number of authors to associate with the article
#         num_authors = random.randint(1, 5)
#         article.authors.set(random.sample(authors, num_authors))
#
#
# create_entreies()

def get_authors(search_name=None, search_email=None):
    if search_name is None and search_email is None:
        return ''
    elif search_name is not None and search_email is not None:
        authors = Author.objects.filter(Q(full_name__icontains=search_name) &
                                        Q(email__icontains=search_email))
    elif search_name is not None:
        authors = Author.objects.filter(full_name__icontains=search_name)
    else:
        authors = Author.objects.filter(email__icontains=search_email)

    authors = authors.order_by('-full_name')

    result = []

    for author in authors:
        status = "Banned" if author.is_banned else "Not Banned"
        result.append(f"Author: {author.full_name}, email: {author.email}, status: {status}")

    return '\n'.join(result) if result else ''


def get_top_publisher():
    top_author = Author.objects \
        .annotate(num_articles=Count('article')) \
        .order_by('-num_articles', 'email') \
        .first()

    if not top_author or not top_author.num_articles:
        return ''

    return f"Top Author: {top_author.full_name} with {top_author.num_articles} published articles."


def get_top_reviewer():
    top_reviewer = Author.objects \
        .annotate(num_reviews=Count('review')) \
        .order_by('-num_reviews', 'email') \
        .first()

    if not top_reviewer or not top_reviewer.num_reviews:
        return ''

    return f"Top Reviewer: {top_reviewer.full_name} with {top_reviewer.num_reviews} published reviews."


def get_latest_article():
    latest_article = Article.objects.order_by('-published_on').first()

    if latest_article is not None:
        authors = latest_article.authors.all().order_by('full_name')
        authors_str = ", ".join(author.full_name for author in authors)
        num_reviews = latest_article.review_set.count()
        avg_reviews_rating = latest_article.review_set.aggregate(avg_rating=Avg('rating'))['avg_rating']

        if not avg_reviews_rating:
            avg_reviews_rating = 0

        return f"The latest article is: {latest_article.title}. Authors: {authors_str}. " \
               f"Reviewed: {num_reviews} times. Average Rating: {avg_reviews_rating:.2f}."
    else:
        return ""


def get_top_rated_article():
    top_rated_article = (
        Article.objects.annotate(avg_rating=Avg('review__rating'))
        .order_by('-avg_rating', 'title')
        .first()
    )

    if not top_rated_article or top_rated_article.avg_rating is None:
        return ''

    num_reviews = top_rated_article.review_set.count()
    return f"The top-rated article is: {top_rated_article.title}, with an average rating of" \
           f" {top_rated_article.avg_rating:.2f}, reviewed {num_reviews} times."


def ban_author(email=None):

    if email is None:
        return "No authors banned."

    try:
        author = Author.objects.get(email=email)
        num_reviews = author.review_set.count()
        author.is_banned = True
        author.save()
        author.review_set.all().delete()

        return f"Author: {author.full_name} is banned! {num_reviews} reviews deleted."
    except Author.DoesNotExist:
        return "No authors banned."


# print(get_authors(search_name='angela', search_email='exa'))
# print(get_top_publisher())
# print(get_top_reviewer())

# print(get_latest_article())
# print(get_top_rated_article())
# print(ban_author(email='hshort@example.org'))
