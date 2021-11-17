from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_safe

from .models import Movie
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
# from random import randint
import random

# Create your views here.
@require_safe
def index(request):
    movies = Movie.objects.all()
    paginator = Paginator(movies, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # /movies/?page=2 ajax 요청 => json
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = serializers.serialize('json', page_obj)
        return HttpResponse(data, content_type='application/json')
    # /movies/ 첫번째 페이지 요청 => html
    else:
        context = {
            'movies': page_obj,
        }

        return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie': movie,
        'url':"https://image.tmdb.org/t/p/original"+movie.poster_path,
        
    }
    return render(request, 'movies/detail.html', context)


@require_safe
def recommended(request):
    movies = Movie.objects.all()
    random_nums = random.sample(range(100),10)
    
    context = {
        'movies': movies,
        'random_nums': random_nums,
    }

    return render(request, 'movies/recommended.html', context)

@require_safe
def recoreco(request):
    
    context = {
        
    }
    

    return render(request, 'movies/recoreco.html', context)