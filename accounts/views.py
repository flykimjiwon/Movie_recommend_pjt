from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm
from django.http import JsonResponse
import random
import requests

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('community:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('community:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'community:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('community:index')


@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    movie_list = person.like_movies.all()
    # genre = movie_list[2].genres.all()
    # 여기서 뽑아내자
    
    #찜한 영화에서 속한 장르에서 무작위 2개골라서 그 2개가 들어간녀석중에 랜덤!
    # num = len(movie_list)
    # num2 = len(genre)
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

    context = {
        'person': person,
        'movie_list':movie_list,
        # 'genre':genre[0].id,
        # 'genre2':genre[0],
        # 'genre3':genre,
        # 'num':num,
        'genre_list':genre_list,
        # 'num2':num2,
        'cnt':cnt,
        'url_key':url_key,
        'result':result[result_num],
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        me = request.user
        you = get_object_or_404(get_user_model(), pk=user_pk)
        if me != you:
            if you.followers.filter(pk=me.pk).exists():
                you.followers.remove(me)
                isFollowed = False
            else:
                you.followers.add(me)
                isFollowed = True
            context = {
                'isFollowed': isFollowed,
                'followers_count': you.followers.count(),
                'followings_count': you.followings.count(),
            }
            return JsonResponse(context)
        return redirect('accounts:profile', you.username)
    return redirect('accounts:login')