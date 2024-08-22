from django.contrib import messages, auth
from django.contrib.auth.models import User
import requests
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect,get_object_or_404
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny

from myapp.serializers import Adminserializers, GenreSerializer, LoginSerializer, MovieSerializer, ReviewSerializer, UserDetailSerializer
from .forms import CategoryForm, MovieForm
from .models import Admintable, Genre, Movie, Review
from django.db.models import Q

class AdminCreateView(generics.ListCreateAPIView):
    queryset = Admintable.objects.all()
    serializer_class = Adminserializers
    permission_classes = [AllowAny]

class AdminLoginView(generics.ListAPIView):
    queryset = Admintable.objects.all()
    serializer_class = LoginSerializer
    
class GenreListCreateAPIView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]

class MovieSearch(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        query = self.request.query_params.get('search', None)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(category__name__icontains=query)
            )            
        
        return queryset

class MovieListCreateAPIView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser:
    #         return Movie.objects.all()
    #     return Movie.objects.filter(added_by=user)
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

class MovieDetail(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieUpdate(generics.RetrieveUpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.added_by:
            serializer.save()

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetail(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class MovieDelete(generics.DestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

def editdetail(request,id):
    api_url = f'http://127.0.0.1:8000/user/{id}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
    return render(request, 'editprofile.html', {'data': data})


def adminregister(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        
        api_url = f'http://127.0.0.1:8000/movieadmin/'

        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            print(data)
            
            if any(user['username'] == username for user in data):
                messages.info(request, 'This username already exists')
                return redirect('adminregister')

            if any(user['email'] == email for user in data):
                messages.info(request, 'This email is already taken')
                return redirect('adminregister')

        if password == confirmpassword:
            register_data = {
                'username': username,
                'email': email,
                'password': password,
            }
            res = requests.post(api_url,data=register_data)
            print(res.status_code)
            
            if res.status_code == 201:  # Created
                messages.info(request, 'Admin created sucessfully')
     
                return redirect('adminlogin')
            else:
                messages.error(request, 'Error registering admin')
                return redirect('adminregister')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('adminregister')

    return render(request, 'admin/adminregister.html')


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        api_url = f'http://127.0.0.1:8000/adminloginpage/'

        # Make the request to the API to get user details
        response = requests.get(api_url, params={'username': username})

        if response.status_code == 200:
            data = response.json()

            # Check if username exists
            if data and any(user['username'] == username for user in data):
                user = next(user for user in data if user['username'] == username)

                # Compare the provided password with the stored password
                if user['password'] == password:  # Ideally use hashed password comparison
                    messages.info(request, 'Login successful')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Wrong password')
                    return redirect('adminlogin')
            else:
                messages.error(request, 'Invalid username')
                return redirect('adminlogin')
        else:
            messages.error(request, 'Error logging in')
            return redirect('adminlogin')

    return render(request, 'admin/adminlogin.html')

def dashboard(request):
    api_url = f'http://127.0.0.1:8000/users/'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        original_data = data
    api_url1 = 'http://127.0.0.1:8000/movies/'

    res = requests.get(api_url1)
    if response.status_code == 200:
        data = res.json()

    return render(request, 'admin/dashboard.html', {'users': original_data,'movies':data})

def movieadmindelete(request, movie_id):
    api_url = f'http://127.0.0.1:8000/delete/{movie_id}/'
    try:
        response = requests.delete(api_url)

        if response.status_code == 200:
            messages.success(request, f'Item with ID {id} has been successfully deleted.')
        else:
            messages.error(request, f'Failed to delete item. Status code: {response.status_code}')

    except requests.RequestException as e:
        messages.error(request, f'Error occurred: {str(e)}')

    return redirect('/dashboard/')

def adminuserdelete(request, user_id):
    api_url = f'http://127.0.0.1:8000/userdelete/{user_id}/'
    try:
        response = requests.delete(api_url)

        if response.status_code == 200:
            messages.success(request, f'Item with ID {id} has been successfully deleted.')
        else:
            messages.error(request, f'Failed to delete item. Status code: {response.status_code}')

    except requests.RequestException as e:
        messages.error(request, f'Error occurred: {str(e)}')

    return redirect('/dashboard/')




def editprofile(request,id):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        api_url = f'http://127.0.0.1:8000/user/{id}/'

        data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password

        }
        response = requests.put(api_url, data=data)

        if response.status_code == 200:
            messages.success(request, 'Profile updated successfully')
            return redirect('/index/')
        else:
            messages.error(request, f'error submitting data to the REST API:{response.status_code}')
    return render(request, 'editprofile.html')

def addcategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                api_url = 'http://127.0.0.1:8000/categories/'
                data = form.cleaned_data
                print(data)

                response = requests.post(api_url, data=data)
                if response.status_code == 400:
                    messages.success(request, f'Category inserted successfully')
                    return redirect('/dashboard')
                else:
                    messages.error(request, f'Error{response.status_code}')
            except requests.RequestException as e:
                messages.error(request, f'Error during API request {str(e)}')
        else:
            messages.error(request, 'form is invalid')
    else:
        form = CategoryForm()
    return render(request, 'admin/addcategory.html', {'form': form})

def addmovie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                api_url = 'http://127.0.0.1:8000/movies/'
                data = form.cleaned_data
                print(data)

                response = requests.post(api_url, data=data, files={'poster': request.FILES['poster']})
                if response.status_code == 400:
                    messages.success(request, f'Movie inserted successfully')
                    return redirect('/index')
                else:
                    messages.error(request, f'Error{response.status_code}')
            except requests.RequestException as e:
                messages.error(request, f'Error during API request {str(e)}')
        else:
            messages.error(request, 'form is invalid')
    else:
        form = MovieForm()
    return render(request, 'addmovie.html', {'form': form})


def moviedetail(request, movie_id):
    api_url = f'http://127.0.0.1:8000/details/{movie_id}/'
    api_url2 = f'http://127.0.0.1:8000/reviews/'
    
    # Fetch movie details
    response = requests.get(api_url)
    original_data = {}
    if response.status_code == 200:
        original_data = response.json()

    # Fetch reviews
    res = requests.get(api_url2)
    newreview = []
    if res.status_code == 200:
        reviews = res.json()
    newreview = [review for review in reviews if review['movie'] == movie_id]

    # Check ownership
    is_owner = False
    if 'added_by' in original_data:
        is_owner = original_data['added_by'] == request.user.id

    # Handle review form submission
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Save the review to the database
        review = Review(
            movie_id=movie_id,  # Associate the review with the movie
            user=request.user,  # Associate the review with the logged-in user
            rating=rating,
            comment=comment
        )
        review.save()
        
        # Redirect to the same movie detail page to see the new review
        return redirect('moviedetail', movie_id=movie_id)
    revstar={1,2,3,4,5,6,7,8,9,10}

    return render(request, 'moviedetail.html', {
        'movie': original_data,
        'is_owner': is_owner,
        'reviews': newreview,
        'star':revstar
    })
   


def update_detail(request, movie_id):
    api_url = f'http://127.0.0.1:8000/details/{movie_id}/'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        original_data = data

    return render(request, 'editmovie.html', {'data': original_data})


def editmovie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.user != movie.added_by:
        return redirect('movie-detail', movie_id=movie_id)

    if request.method == "POST":
        movie.title = request.POST.get('title')
        movie.description = request.POST.get('description')
        movie.release_date = request.POST.get('release_date')
        movie.actors = request.POST.get('actors')
        movie.trailer_link = request.POST.get('trailer_link')

        if 'poster' in request.FILES:
            movie.poster = request.FILES['poster']
        
        movie.save()
        return redirect('moviedetail', movie_id=movie.id)

    return render(request, 'editmovie.html', {'data': movie})

def moviedelete(request, movie_id):
    api_url = f'http://127.0.0.1:8000/delete/{movie_id}'
    response = requests.delete(api_url)

    if response.status_code == 200:
        print(f'Item with id {movie_id} has been deleted')

    else:
        print(f'Failed to delete item status code {response.status_code}')
    return redirect('index')



def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if password == password1:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request, 'This email already taken')
                return redirect('register')

            else:
                user = User.objects.create_user(username=username, first_name=first_name,
                                                last_name=last_name, email=email,
                                                password=password)
                user.save()
                return redirect('login')

        else:
            messages.info(request, 'Password does not match')
            return redirect('register')

    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('welcome')
        else:
            messages.info(request, "please provide correct credentials")
            return redirect('/')

    return render(request, 'login.html')

def welcome(request):
    return render(request,'welcome.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def adminlogout(request):
    auth.logout(request)
    return redirect('/adminlogin/')



def index(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        api_url = f'http://127.0.0.1:8000/search/?search={search}'       
        try:
            response = requests.get(api_url)
            print(response.status_code)
            if response.status_code == 200:
                data = response.json()
                print(data)
            else:
                data = None
        except requests.RequestException:
            data = None
        return render(request, 'index.html', {'movies': data})

    else:
        api_url = 'http://127.0.0.1:8000/movies/'
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                original_data = response.json()
                paginator = Paginator(original_data, 6)

                page = request.GET.get('page', 1)
                try:
                    movies = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    movies = paginator.page(paginator.num_pages)

                context = {
                    'movies': movies,
                }
                return render(request, 'index.html', context)
            else:
                return render(request, 'index.html', {'error_message': f'Error: {response.status_code}'})
        except requests.RequestException as e:
            return render(request, 'index.html', {'error_message': f'Error: {str(e)}'})
