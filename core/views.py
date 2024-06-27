import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Movie, MovieList
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def index(request):
    movies = Movie.objects.all()
    featured_movie = movies[len(movies)-1]

    context = {
        'movies': movies,
        'featured_movie': featured_movie,
    }
    return render(request, 'index.html', context)


@login_required(login_url='login')
def movie(request, pk):
    movie_uuid = pk
    movie_details = Movie.objects.get(uu_id=movie_uuid)

    context = {
        'movie_details': movie_details
    }

    return render(request, 'movie.html', context)


@login_required(login_url='login')
def genre(request, pk):

    movie_genre = pk
    movies = Movie.objects.filter(genre=movie_genre)

    context = {
        'movie_genre_FE': movie_genre,
        'movies_FE': movies

    }

    return render(request, 'genre.html', context)

@login_required(login_url='login')
def search(request):
    if request.method == 'POST':
        search_term = request.POST['search_term']
        movies = Movie.objects.filter(title__icontains=search_term)

        context = {
            'movies': movies,
            'search_term': search_term,
        }
        return render(request, 'search.html', context)
    else:
        return redirect('/')


@login_required(login_url='login')
def my_favourite(request):

    movie_list = MovieList.objects.filter(owner_user=request.user)
    user_movie_list = []

    for movie in movie_list:
        user_movie_list.append(movie.movie)

    context = {
        'favourite_movies': user_movie_list  # Corrected variable name
    }
    return render(request, 'my_favourite.html', context)


def check_favourite(request):
    if request.method == 'POST' and request.is_ajax():
        movie_id = request.POST.get('movie_id')
        user = request.user
        movie = get_object_or_404(Movie, uu_id=movie_id)
        if MovieList.objects.filter(user=user, movies__uu_id=movie_id).exists():
            return JsonResponse({'status': 'exists', 'message': 'Movie already in favorites.'})
        else:
            return JsonResponse({'status': 'not_exists', 'message': 'Movie not in favorites yet.'})
    return JsonResponse({'error': 'Invalid request.'}, status=400)


@login_required(login_url='login')
def add_to_favourite(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None

        movie = get_object_or_404(Movie, uu_id=movie_id)
        movie_list, created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)

        if created:
            response_data = {'status': 'success', 'message': 'Added ✓'}
        else:
            response_data = {'status': 'info', 'message': 'Movie already in list'}

        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['input_username']
        password = request.POST['input_password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            # messages.info(request, 'Invalid Login Credentials')
            # return redirect('/')
            messages.info(request, 'Invalid Login Credentials')
            context = {'messages': messages.get_messages(request)}  # Get messages
            return render(request, 'login.html', context)  # Render login with context
    else:
        return render(request, 'login.html')
    

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['input_email']
        username = request.POST['input_username']
        password = request.POST['input_password']
        password2 = request.POST['input_password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #Log in user
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password Do Not Match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')