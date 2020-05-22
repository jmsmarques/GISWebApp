from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from django.core.serializers import serialize
from .models import Parish, ImagePoint, Municipality
from .forms import ImagePointForm

def index(request):
    if not request.user.is_authenticated:
        return render(request, "gisMap/login.html")
    #set context to include all the images in the database
    context = {
        "user": request.user,
        "images": ImagePoint.objects.all(),
        "form": ImagePointForm()
    }
    return render(request, "gisMap/index.html", context)

@require_http_methods(["POST"])
def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"), {"user": request.user, "form": ImagePointForm()})
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

    context = {
        "user": request.user,
        "form": ImagePointForm()
    }

    return render(request, "gisMap/index.html")

@require_http_methods(["POST"])
def add_image(request):
    if not request.user.is_authenticated: #verify that the user is logged in
        return render(request, "gisMap/login.html")
    
    message = None  #Message to send to user in case of failure
    try:
        form = ImagePointForm(request.POST, request.FILES)
        if form.is_valid():
            description = request.POST["description"]
            author_id = request.POST["author"]
            author = User.objects.get(id=author_id)
            lat = float(request.POST["lat"])
            lon = float(request.POST["lon"])
            location = Point(lon, lat)

            #upload the image
            image = request.FILES["image"]

            #intersect the location with the parish_names to find in which one it is located
            parish_name = Parish.objects.get(geom__contains=location)

            new_image = ImagePoint(description=description, author=author, image=image, location=location, parish_name=parish_name)
            new_image.save()
            message = "Point added"
    except Exception as e:
        print(f"Point addition failed because {e}")
        message = "Point addition failed"
        
    #set context to include all the images in the database
    context = {
        "user": request.user,
        "images": ImagePoint.objects.all(),
        "message": message,
        "form": ImagePointForm()
    }

    return render(request, "gisMap/index.html", context)

@require_http_methods(["POST"])
def remove_image(request):
    if not request.user.is_authenticated: #verify that the user is logged in
        return render(request, "gisMap/login.html")

    message = None  #Message to send to user in case of failure

    try:
        img_id = request.POST["img_id"]
        #search for the image in the database and delete it
        ImagePoint.objects.get(id=img_id).delete()
        message = "Image removal successful"
    except Exception as e:
        print(f"Point remove failed because {e}")
        message = "Point removal failed"

    #set context to include all the images in the database
    context = {
        "user": request.user,
        "images": ImagePoint.objects.all(),
        "message": message,
        "form": ImagePointForm()
    }

    return render(request, "gisMap/index.html", context)

def download_image(request): #function that allows the download of an image
    if not request.user.is_authenticated: #verify that the user is logged in
        return render(request, "gisMap/login.html")

    message = None  #Message to send to user in case of failure

    #prepare geojson for download
    img_id = request.POST["img_id"] #img to download

    file_to_download = serialize('geojson', [ImagePoint.objects.get(id=img_id),], 
        geometry_field = 'point',
        fields = ['parish_name', 'parish_name.concelho', 'image', 'location']
    )

    print(file_to_download)

    context = {
        "user": request.user,
        "images": ImagePoint.objects.all(),
        "message": message,
        "form": ImagePointForm()
    }

    return render(request, "gisMap/index.html", context)