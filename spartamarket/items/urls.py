from django.urls import path
from . import views

app_name = 'items'
urlpatterns = [
    path('', views.items, name='items'),
    path('hello/', views.hello, name='hello'),
    path('data-throw/', views.data_throw, name='throw'),
    path('data-catch/', views.data_catch, name='catch'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    #
    path('index/', views.index, name='index'),
    #
    path('<int:pk>/delete/', views.delete, name='delete'),
    path("<int:pk>/update/", views.update, name="update"),
    path('create/', views.create, name='create'),

    path("<int:pk>/comments/", views.comment_create, name="comment_create"),
    path("<int:pk>/delete_comment/", views.delete_comment, name="delete_comment"),

    path("<int:pk>/like/", views.like, name="like"),
]
