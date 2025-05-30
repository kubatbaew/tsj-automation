from django.urls import path, include

from apps.pages.views import login_logics, homepage, history_buy, logout_logics


urlpatterns = [
    path('', homepage, name="homepage"),
    path('login/', login_logics, name="login_logics"),
    path('history_buy/', history_buy, name="history_buy"),
    path('logout/', logout_logics, name="logout_logics"),
]
