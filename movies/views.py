from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_safe, require_POST

from .models import Movie, MovieComment
from .forms import MovieCommentForm
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse, JsonResponse
# from random import randint
import random
import requests

# Create your views here.
@require_safe
def index(request):
    #movies = Movie.objects.all()
    movies = Movie.objects.order_by('?')
    # 미쳤다~~ 이렇게 되는구낭

    #my_list = list(movies)
    #random.shuffle(my_list)
    # movies = random.shuffle(movies)
    context = {
        'movies':movies,
    }

    # paginator = Paginator(movies, 10)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # # /movies/?page=2 ajax 요청 => json
    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     data = serializers.serialize('json', page_obj)
    #     return HttpResponse(data, content_type='application/json')
    # # /movies/ 첫번째 페이지 요청 => html
    # else:
    #     context = {
    #         'movies': page_obj,
    #     }

    #     return render(request, 'movies/index.html', context)
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment_form = MovieCommentForm()
    comments = movie.moviecomment_set.all()
    context = {
        'movie': movie,
        'url':"https://image.tmdb.org/t/p/original"+movie.poster_path,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'movies/detail.html', context)

@require_safe
def detail2(request, movie_list_id):
    url='https://api.themoviedb.org/3/movie/'+str(movie_list_id)+'?api_key=7c6377fdbf40d8566d0e591005c3dad5&language=ko-KR'
    response=requests.get(url).json()
    context = {
        'movie': response,        
    }
    return render(request, 'movies/detail2.html', context)

@require_safe
def recommended(request):
    movies = Movie.objects.all()
    random_nums = random.sample(range(100),10)
    context = {
        'movies': movies,
        'random_nums': random_nums,
    }
    return render(request, 'movies/recommended.html', context)

# @require_safe
def recoreco(request):
    movies = Movie.objects.all()
    genre = {
    '모험':'12',
    '판타지':'14',
    '애니':'16',
    '드라마':'18',
    '공포':'27',
    '액션':'28',
    '코미디':'35',
    '역사':'36',
    '서부':'37',
    '스릴러':'53',
    '범죄':'80',
    '다큐':'99',
    'SF':'878',
    '추리':'9648',
    '음악':'10402',
    '로맨스':'10749',
    '가족':'10751',
    '전쟁':'10752',
    'TV':'10770',
    }
    context = {
        'movies':movies[0],
        'genre':genre,
    }
    # url='https://api.themoviedb.org/3/discover/movie?api_key=7c6377fdbf40d8566d0e591005c3dad5&language=ko-KR&with_genres='+url_key+'&sort_by=popularity.desc'
    # response=requests.get(url).json()
    
    return render(request, 'movies/recoreco.html', context)

# @require_safe
def result(request):
    # value = request
    # value2 = request.GET
    # value3 = request.method
    # value4 = request.GET['search']
    result = request.GET['search']
    result_key=result.split(',')
    genre = {
    '모험':'12',
    '판타지':'14',
    '애니':'16',
    '드라마':'18',
    '공포':'27',
    '액션':'28',
    '코미디':'35',
    '역사':'36',
    '서부':'37',
    '스릴러':'53',
    '범죄':'80',
    '다큐':'99',
    'SF':'878',
    '추리':'9648',
    '음악':'10402',
    '로맨스':'10749',
    '가족':'10751',
    '전쟁':'10752',
    'TV':'10770',
    }
    url_key=''
    for i in range(len(result_key)-1):
        url_key += genre[result_key[i]]+','
    flag = False
    for i in range(len(result_key)-1):
        if result_key[i] in genre:
            flag=True
        else:
            flag=False
    if flag:
        genre_ids=genre[result_key[0]]
        url='https://api.themoviedb.org/3/discover/movie?api_key=7c6377fdbf40d8566d0e591005c3dad5&language=ko-KR&with_genres='+url_key+'&sort_by=popularity.desc'
    else:
        genre_ids=''
        url='https://api.themoviedb.org/3/discover/movie?api_key=7c6377fdbf40d8566d0e591005c3dad5&language=ko-KR&sort_by=popularity.desc'
    
    response=requests.get(url).json()
    movie_lists=response["results"]
    # results는 json파일에 안에있는 키값
    # 뭐시기... json파일 파싱해오기

    context = {
        # 'value':value,
        # 'value2':value2,
        # 'value3':value3,
        # 'value4':value4,
        'result':result,
        'url':url,
        'genre_ids':genre_ids,
        'result_key':result_key,
        'url_key':url_key,
        # 'response':response,
        'movie_lists':movie_lists,
    }
    return render(request, 'movies/result.html', context)


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        comment_form = MovieCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
        # context = {
        #     'comment': comment
        # }
        # return JsonResponse()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, movie_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(MovieComment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:detail', movie_pk)

@require_POST
def like(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        # 현재 좋아요를 요청하는 회원이
        # 해당 게시글의 좋아요를 누른 회원 목록에 이미 있다면,
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user) # 좋아요 취소
            liked = False
        else:   # 없다면 좋아요 하기
            movie.like_users.add(request.user)
            liked = True
        context = {
            'liked': liked,
            'count': movie.like_users.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:login')




