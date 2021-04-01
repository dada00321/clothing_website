from django.urls import path
from . import views

app_name = "search"
urlpatterns = [
    path("", views.post_search, name="post_search"),
]
