import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from functools import wraps

from apps.months.models import Year, PaidMonth, Month

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


def logout_logics(request):
    logout(request)
    return redirect("login_logics")


@_check_is_authenticated
def homepage(request):
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    
    year_obj = Year.objects.get(year=now_year)
    month_obj = Month.objects.get(year=year_obj, month=now_month)


    paid_month = PaidMonth.objects.get(
        apartment=request.user.apartment,
        month=month_obj,
    )

    print(paid_month)

    return render(request, 'index.html', locals())


@_check_is_authenticated
def history_buy(request):
    now_year = datetime.datetime.now().year
    now_month = datetime.datetime.now().month
    year_obj = Year.objects.get(year=now_year)
    
    paid_to_month = []
    months = year_obj.months_for_year.all()
    for month in months:
        paid = PaidMonth.objects.get(
            month=month,
            apartment=request.user.apartment,
        )
        paid_to_month.append(paid)
    

    return render(request, "history.html", locals())
