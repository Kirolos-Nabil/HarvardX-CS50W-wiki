from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("createNewEntry", views.createNewEntry, name="createNewEntry"),
    path("random", views.random, name="random")
]
