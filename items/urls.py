from django.urls import path
from . import views

app_name = 'items'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('item_detail/<int:id>/', views.item_detail, name='item_detail'),
    path('register/', views.register, name='register'),
    path('check_register/', views.check_register, name='check_register'),
    path('do_register/', views.do_register, name='do_register'),
    path("delete/<int:id>/", views.delete, name="delete"),
    path("update/<int:id>/", views.update, name="update"),
    path("like/<int:id>/", views.like, name="like"),
]
