from rest_framework import serializers
from .models import Admintable, Genre, Movie, Review
from django.contrib.auth.models import User

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','password'] 

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    category= GenreSerializer(read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password'] 

class ReviewSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

class Adminserializers(serializers.ModelSerializer):
    class Meta:
        model = Admintable
        fields = '__all__'

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admintable
        fields = ('username','password')

