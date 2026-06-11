from django.shortcuts import render, redirect
from django.db import connection
from .models import Users, Cities
from django.contrib.auth.hashers import make_password

def login_view(request):

    error = None

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Users.objects.get(
                email=email,
                password=password
            )

            request.session['user_id'] = user.user_id

            return redirect('home')

        except Users.DoesNotExist:
            error = "Սխալ email կամ password"

    return render(
        request,
        "pharmacy/login.html",
        {"error": error}
    )


def register(request):

    cities = Cities.objects.all()

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        age = request.POST.get("age")
        city_id = request.POST.get("city")

        city = Cities.objects.get(
            city_id=city_id
        )

        user = Users(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),
            age=age,
            city=city
        )

        user.save()

        request.session['user_id'] = user.user_id

        return redirect('home')

    return render(
        request,
        "pharmacy/register.html",
        {
            "cities": cities
        }
    )


def home(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    try:
        user = Users.objects.get(
            user_id=user_id
        )

    except Users.DoesNotExist:
        return redirect('login')

    medicines = []

    if request.method == "POST":

        symptom = request.POST.get("symptom")

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT m.Medicine_Name
                FROM Symptom_Medicines sm
                JOIN Medicines m
                ON sm.Medicine_ID = m.Medicine_ID
                WHERE LOWER(sm.Symptom_Name) = LOWER(%s)
            """, [symptom])

            medicines = cursor.fetchall()

    return render(
        request,
        "pharmacy/home.html",
        {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "medicines": medicines
        }
    )


def logout_view(request):

    request.session.flush()

    return redirect('login')