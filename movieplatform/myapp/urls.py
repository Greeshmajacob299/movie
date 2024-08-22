from django.urls import path
from myapp import views
from .views import *


urlpatterns = [
    path('index/',views.index,name='index'),
    path('register/', views.register_user, name='register'),
    path('', views.login_user, name='login'),
    path('user/<int:pk>/',UserDetailView.as_view(),name='user'),
    path('users/',UserView.as_view(),name='users'),
    path('userdelete/<int:pk>/',UserDelete.as_view(),name='movie-delete'),
    path('movieadmin/',AdminCreateView.as_view(),name='admin'),
    path('adminloginpage/',AdminLoginView.as_view(),name='admin-login'),
    path('movies/', MovieListCreateAPIView.as_view(), name='movie-list-create'),
    path('details/<int:pk>/', MovieDetail.as_view(), name='movie-detail'),
    path('update/<int:pk>/', MovieUpdate.as_view(),name='movie-update'),
    path('delete/<int:pk>/',MovieDelete.as_view(),name='movie-delete'),
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('search/', MovieSearch.as_view(), name='movie-search'),   
    path('reviewdetail/<int:pk>/',ReviewDetail.as_view(),name='reviewdetails'),
    path('categories/', GenreListCreateAPIView.as_view(), name='category-list-create'),
    path('addmovie/',views.addmovie,name='addmovie'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('logout/',views.logout,name='logout'),
    path('update_detail/<int:movie_id>/',views.update_detail,name='update_detail'),
    path('moviedetail/<int:movie_id>/',views.moviedetail,name='moviedetail'),
    path('moviedelete/<int:movie_id>/',views.moviedelete,name='moviedelete'),
    path('movieadmindelete/<int:movie_id>/',views.movieadmindelete,name='movieadmindelete'),
    path('updatemovie/<int:movie_id>/',views.editmovie,name='updatemovie'),
    path('editdetail/<int:id>/',views.editdetail,name='editdetail'),
    path('editprofile/<int:id>/',views.editprofile,name='editprofile'),
    path('welcome/',views.welcome,name='welcome'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminregister/',views.adminregister,name='adminregister'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('adminuserdelete/<int:user_id>/',views.adminuserdelete,name='adminuserdelete'),
    path('addcategory',views.addcategory,name='addcategory')

]