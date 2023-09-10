from django.urls import path, re_path

from .views import HomeView, redirect_url


urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    re_path(r'^(?P<hashed_url>[a-zA-Z0-9]+)/$', redirect_url)
]
