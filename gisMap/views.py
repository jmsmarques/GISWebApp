from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from .models import Freguesia, Image, Concelho

def index(request):
    if not request.user.is_authenticated:
        return render(request, "gisMap/login.html")
    return render(request, "gisMap/index.html")

@require_http_methods(["POST"])
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "gisMap/login.html", {"message": "Invalid credentials"})

def logout_view(request):
    logout(request)
    return render(request, "gisMap/login.html", {"message": "Logged out"})

@require_http_methods(["POST"])
def register_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]

    user = User.objects.create_user(username=username, email=email, password=password)

    user.save()

    login(request, user) #login the newly registered user
    return render(request, "gisMap/index.html")


def add_image(request):
    if not request.user.is_authenticated: #verify that the user is logged in
        return render(request, "gisMap/login.html")
    
    description = request.POST["description"]
    image = request.POST.get("image", None)
    lat = float(request.POST["lat"])
    lon = float(request.POST["lon"])
    location = Point(lon, lat)

    #intersect the location with the freguesias to find in which one it is located
    freguesia = Freguesia.objects.get(geom__contains=location)

    new_image = Image(description=description, image=image, location=location, freguesia=freguesia)
    new_image.save()
    return render(request, "gisMap/index.html")

