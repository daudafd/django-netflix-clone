from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('movie/<str:pk>/', views.movie, name='movie'),
    path('genre/<str:pk>/', views.genre, name='genre'),
    path('my-favourite/', views.my_favourite, name='my-favourite'),
    path('check-favourite/', views.check_favourite, name='check_favourite'),
    path('add-to-favourite/', views.add_to_favourite, name='add-to-favourite'),
    # path('toggle_favorite/<int:movie_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.search, name='search'),

]                                                                                   