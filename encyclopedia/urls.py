from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="indexWiki"),
    path("wiki/<str:title>/", views.content, name="content"), # /wiki/title
]
