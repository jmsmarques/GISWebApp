from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from django.core.serializers import serialize
from .models import Parish, ImagePoint, Municipality
from .forms import ImagePointForm
from zipfile import ZipFile
from io import BytesIO, StringIO
import os, geojson, tempfile

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
    mousepos = None #Point added position, used to keep the map view on place on reload

    try:
        form = ImagePointForm(request.POST, request.FILES)
        if form.is_valid():
            description = request.POST["description"]
            author_id = request.POST["author"]
            author = User.objects.get(id=author_id)
            lat = float(request.POST["lat"])
            lon = float(request.POST["lon"])
            location = Point(lon, lat)
            mousepos = location
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
        "form": ImagePointForm(),
        "mousepos": mousepos
    }

    return render(request, "gisMap/index.html", context)

@require_http_methods(["POST"])
def remove_image(request):
    if not request.user.is_authenticated: #verify that the user is logged in
        return render(request, "gisMap/login.html")

    message = None  #Message to send to user in case of failure
    mousepos = None #Point added position, used to keep the map view on place on reload

    try:
        img_id = request.POST["img_id"]
        #search for the image in the database and delete it
        img = ImagePoint.objects.get(id=img_id)
        mousepos = img.location
        img.delete() #delete from database
        message = "Image removal successful"
    except Exception as e:
        print(f"Point remove failed because {e}")
        message = "Point removal failed"

    #set context to include all the images in the database
    context = {
        "user": request.user,
        "images": ImagePoint.objects.all(),
        "message": message,
        "form": ImagePointForm(),
        "mousepos": mousepos
    }

    return render(request, "gisMap/index.html", context)

def download_image(request): #function that allows the download of an image
    if not request.user.is_authenticated: #verify that the user is logged in
        return render(request, "gisMap/login.html")

    message = None  #Message to send to user in case of failure

    #prepare geojson for download
    img_id = request.POST["img_id"] #img to download

    img = ImagePoint.objects.get(id=img_id)

    img_info = geojson.Feature(geometry= geojson.Point((img.location.x, img.location.y)),
                            properties = {"District": str.title(img.parish_name.municipality_name.district_name.district_name),
                                            "Municipality": str.title(img.parish_name.municipality_name.municipality_name),
                                            "Parish": img.parish_name.parish_name})
    features = []
    features.append(img_info)
    file_to_download = geojson.FeatureCollection(features)
    #endof json preparation

    mem_file = BytesIO() #memory where the zip file will be created
    with ZipFile(mem_file, 'w') as zipFolder: #create a zipped folder to return to the user
        zipFolder.writestr('image_data.geojson', geojson.dumps(file_to_download))
        zipFolder.write(settings.BASE_DIR + img.image.url, 'image.jpeg')

    mem_file.seek(0)
    response = HttpResponse(mem_file.read(), content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename="%s.zip"'%img
    return response