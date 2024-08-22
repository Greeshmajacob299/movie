from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='posters/')
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=255)
    category = models.ForeignKey(Genre, on_delete=models.CASCADE)
    trailer_link = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f'Review of {self.movie.title} by {self.user.username}'
    

class Admintable(models.Model):
    email=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=10)

    
class Login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=10)

   