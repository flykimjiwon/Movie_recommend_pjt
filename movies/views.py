from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_safe, require_POST
from django.contrib.auth.decorators import login_required

from .models import Movie, MovieComment
from .forms import MovieCommentForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model

import requests
import random
# Create your views here.
@require_safe
def index(request):
    username = request.user
    person = get_object_or_404(get_user_model(), username=username)
    movie_like = person.like_movies.all()
    movies = Movie.objects.order_by('?')
    
    a = list(movies)
    b = list(movie_like)
    c = list(set(a)-set(b))
    random.shuffle(c)
    # DB전체 영화중, 찜하지않은 목록만 보여주기위함,그리고 무작위로

    context = {
        'movie_like':movie_like,
        'person':person,
        'movies':movies,
        'c':c[:18],
        # 찜하지않은 영화중에 18개만 보여준다.
        
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movies = Movie.objects.all()
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment_form = MovieCommentForm()
    comments = movie.moviecomment_set.all()
    context = {
        'movies': movies,
        'movie': movie,
        'url':"https://image.tmdb.org/t/p/w780"+movie.poster_path,
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
    movie = Movie.objects.order_by('?')[0]
    context = {
        'movie': movie,
    }
    return render(request, 'movies/recommended.html', context)

@login_required
def blackbean(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    movie_list = person.like_movies.all()
    genre_list=[]
    cnt=0
    for i in range(len(movie_list)):
        for j in range(len(movie_list[i].genres.all())):
            cnt+=1
            genre_list.append(movie_list[i].genres.all()[j].id) 

    genre_list = list(set(genre_list))
    if len(genre_list) !=0:
        genre_list = random.sample(genre_list,2)
    else:
        genre_list = []
    url_key=''
    for i in range(len(genre_list)):
        url_key += str(genre_list[i])+','

    url='https://api.themoviedb.org/3/discover/movie?api_key=7c6377fdbf40d8566d0e591005c3dad5&language=ko-KR&with_genres='+url_key+'&sort_by=popularity.desc'
    response=requests.get(url).json()
    result = response["results"]
    random_len = len(result)
    result_num = random.randrange(0,random_len)
    result = result[0:4]
    random.shuffle(result)
    movies = Movie.objects.order_by('?')
    context = {
        'person': person,
        'movie_list':movie_list,
        'genre_list':genre_list,    
        'cnt':cnt,
        'url_key':url_key,
        'results':result,
        # 'test':result[result_num],
        'movies': movies,
    }
    return render(request, 'movies/blackbean.html', context)

            

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

@require_POST
def unlike(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user) # 좋아요 취소
        else:   # 없다면 좋아요 하기
            movie.like_users.add(request.user)
        return redirect('accounts:profile', request.user)
