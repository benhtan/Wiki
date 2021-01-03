from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.content, name="content"), # /wiki/title
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
]
