from .managers import MovieManager
from django.db import models


class Movie(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=50)
    storyline = models.TextField()
    similar_movies = models.CharField(max_length=255)

    objects = MovieManager()
    indexes = [
        models.Index(fields=['code', 'title', 'storyline', ]),
    ]


class MoviePhotoCollection(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    photo = models.CharField(max_length=255)
