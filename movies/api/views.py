from . import serializers as serial
from rest_framework.views import APIView
from accounts.models import User
from rest_framework import permissions, status, generics, mixins
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from movies import models
import requests
from requests.auth import HTTPBasicAuth
from decouple import config
from urllib.parse import urlparse, urlencode
from django.urls import reverse
from movies.utils import make_retry
from collections import Counter


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }


class RegisterUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serial.UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                response = get_tokens_for_user(user)
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(
                {"error": "User with this username already exists!"},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serial.UserAuthSerializer(data=request.data)
        if serializer.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,
                                username=username,
                                password=password)
            if user:
                response = get_tokens_for_user(user)
                return Response(response, status=status.HTTP_200_OK)

            user = User.objects.filter(username=username).first()
            if not user:
                return Response(
                    {"error": "Please provide correct username!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {'error': 'Gimport requests Password is not correct!'},
                    status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ListMoviesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, **kwargs):
        self.session = make_retry(session=requests.Session())
        return super().__init__(**kwargs)

    def get(self, request):
        username = config('CREDY_USERNAME', '')
        password = config('CREDY_PASSWORD', '')
        movies_url = config('MOVIE_LIST_URL')

        if request.query_params:
            query_params = request.query_params
            query_string = urlencode(query_params)
            movies_url = f'{movies_url}?{query_string}'

        response = self.session.get(movies_url,
                                    auth=HTTPBasicAuth(username, password),
                                    verify=False)

        if response.status_code == 200:
            data = response.json()
            base_url = request.build_absolute_uri(reverse('movie-list'))

            if data['next']:
                url1 = data['next']
                parsed_url1 = urlparse(url1)
                query_string1 = parsed_url1.query
                data['next'] = f'{base_url}?{query_string1}'

            if data['previous']:
                url2 = data['previous']
                parsed_url2 = urlparse(url2)
                query_string2 = parsed_url2.query
                data['previous'] = f'{base_url}?{query_string2}'

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'Error': {response.text}},
                            status=response.status_code)


def get_top_three_genres(movies):
    genre_counter = Counter()
    for movie in movies:
        if movie.genres:
            genres_list = movie.genres.split(',')
            genre_counter.update(genre.strip() for genre in genres_list)
    top_three_genres = [genre for genre, count in genre_counter.most_common(3)]
    return top_three_genres


class CollectionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serial.CollectionListSerializer
    queryset = models.Collection.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        response = serial.CollectionCreateSerializer(
                        data=request.data, context={'request': request})
        response.is_valid(raise_exception=True)
        instance = response.save()
        return Response({'collection_uuid': instance.uuid},
                        status=status.HTTP_201_CREATED)

    def get(self, request):
        try:
            movies = models.Movie.objects.filter(collection__user=request.user)
            response = self.get_serializer(self.get_queryset(), many=True)
            response = {
                "is_success": True,
                "data":
                    {
                        "collections": response.data,
                        "favourite_genres": get_top_three_genres(movies)
                    }
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"is_success": False, "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST)


class CollectionManageView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serial.CollectionCreateSerializer
    queryset = models.Collection.objects.all()
