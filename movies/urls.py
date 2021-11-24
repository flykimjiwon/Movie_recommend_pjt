from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('recommended/', views.recommended, name='recommended'),
    path('recoreco/', views.recoreco, name='recoreco'),
    path('result/', views.result, name='result'),
    path('blackbean/<username>/', views.blackbean, name='blackbean'),
    path('suggest/<int:movie_list_id>/', views.detail2, name='detail2'),

    path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:movie_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/unlike/', views.unlike, name='unlike'),

]
