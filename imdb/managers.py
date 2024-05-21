from django.db import models
from django.db.models import Q


class MovieManager(models.Manager):
    def search(self, search_string):
        return self.get_queryset().filter(
            Q(title__contains=search_string) |
            Q(storyline__contains=search_string) |
            Q(code__contains=search_string)
        )
