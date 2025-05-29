from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from functools import wraps

def _check_is_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login_logics')
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view




def login_logics(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if not remember_me:
                request.session.set_expiry(0)

            return redirect('homepage')
        else:
            messages.error(request, "Неверное имя пользователя или пароль")

    return render(request, "login.html")


@_check_is_authenticated
def homepage(request):

    return render(request, 'index.html', locals())


@_check_is_authenticated
def history_buy(request):
    
    return render(request, "history.html", locals())
