from accounts.models import User
from rest_framework import serializers
from movies.models import Collection, Movie


class UserAuthSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'genres', 'uuid', 'collection']
        extra_kwargs = {'collection': {'write_only': True, "required": False}}


class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'uuid', 'description']


class CollectionCreateSerializer(serializers.ModelSerializer):
    movies = MoviesSerializer(many=True, required=False)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        movies = validated_data.pop('movies') \
            if validated_data.get('movies') else []
        collection = super().create(validated_data)
        try:
            for movie in movies:
                movie['collection'] = collection.uuid
            movies = MoviesSerializer(data=movies, many=True)
            movies.is_valid(raise_exception=True)
            movies.save()
            return collection
        except Exception as e:
            collection.delete()
            raise serializers.ValidationError(str(e))

    def update(self, instance, validated_data):
        movies = validated_data.pop('movies') \
            if validated_data.get('movies') else []
        collection = super().update(instance, validated_data)
        try:
            if movies:
                for movie in collection.movies.all():
                    movie.delete()
            for movie in movies:
                movie['collection'] = collection.uuid
            movies = MoviesSerializer(data=movies, many=True)
            movies.is_valid(raise_exception=True)
            movies.save()
            return collection
        except Exception as e:
            raise serializers.ValidationError(str(e))
