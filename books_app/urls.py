from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('main', views.main),
    path('add_book', views.add_book),
    path('user/<int:user_id>', views.user_page),
    path('book/<int:book_id>', views.book),
    path("favorite/<int:book_id>", views.favorite),
    path("unfavorite/<int:book_id>", views.unfavorite),
    path('delete_book/<int:book_id>', views.delete),
    path('edit_book/<int:book_id>', views.edit)
]