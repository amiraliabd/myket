from rest_framework import serializers
from .cruller_core import CrullerCore
from .models import Movie, MoviePhotoCollection


class PhotoSerializer(serializers.Serializer):
    photo = serializers.CharField(max_length=255)


class MovieSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['code',
                  'title',
                  'storyline',
                  'similar_movies',
                  'photos',
                  ]
        extra_kwargs = {
            'title': {'read_only': True},
            'storyline': {'read_only': True},
            'similar_movies': {'read_only': True},
        }

    def create(self, validated_data):
        code = validated_data.pop('code')
        if existing := Movie.objects.filter(code=code).first():
            return existing

        cruller = CrullerCore(code)

        similar_movies_list = cruller.get_similar()
        similar_movies = ", ".join(similar_movies_list)
        movie = Movie.objects.create(
            title=cruller.get_title(),
            storyline=cruller.get_storyline(),
            similar_movies=similar_movies,
            code=code,
        )
        for image in cruller.get_images():
            MoviePhotoCollection.objects.create(movie=movie, photo=image)

        return movie

    def to_representation(self, instance):
        result = super().to_representation(instance)
        related_images = MoviePhotoCollection.objects.filter(movie=instance).all()
        result['photos'] = [image.photo for image in related_images]
        return result

