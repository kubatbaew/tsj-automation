from django.urls import path, include

from apps.pages.views import login_logics, homepage


urlpatterns = [
    path('', homepage, name="homepage"),
    path('login/', login_logics, name="login_logics"),
]
