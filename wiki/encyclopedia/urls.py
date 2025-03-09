from django.urls import path

from . import views
app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("new/", views.new, name="new"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("random/", views.random_page, name="random"),
]
